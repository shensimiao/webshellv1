from __future__ import absolute_import, division, with_statement


import os
import re
import select
import typing
import datetime
import async_timeout
import asyncio

from subprocess import Popen, PIPE
from collections import OrderedDict


from typing import (
    Any,
    Dict,
    Callable,
    Type,
    Tuple,
    Optional,
    Union,
    NoReturn,
    TypeVar,

)

if typing.TYPE_CHECKING:
    from types import TracebackType


__all__ = [
    'BASE_DIR',
    'PIDFile',
    'load_protocol',
    'maybe_int',
    'maybe_split',
    'run',
    'async_run_shell',
    'STDOUT',
    'STDERR',
    'RUN_CMD_TIMEOUT',
    'convert_traffic_from_byte',
    'convert_traffic_to_byte',
    'BINARY_SCALE',
    'DECIMAL_SCALE',
    'UNITS',
    'import_object',
    'errno_from_exception',
    'raise_exc_info',
    'Configurable',
    'PackIp',
    'IPv4Type',
    'to_timestamp_seconds',
    'record_exception_to_logger',
    'STDERRException'
]

STDOUT = 1
STDERR = 2
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
RUN_CMD_TIMEOUT = 60
verbose = 1





def load_protocol() -> dict:
    protocols = {}
    with open("/etc/protocols", "r", encoding="utf-8") as f:
        for line in f.readlines():
            if not line.strip():
                continue
            if line.startswith("#"):
                continue
            proto, num, _ = line.split(None, 2)
            protocols[int(num)] = proto
    protocols[0] = 'ip'
    return protocols

def maybe_int(val):
    try:
        val = int(val)
    except (TypeError, ValueError):
        pass
    return val

def maybe_split(val, sep):
    if hasattr(val, 'split'):
        return val.split(sep)
    return val

def run_command(cmds: Union[str, list]):
    if isinstance(cmds, list):
        cmds = ' '.join(cmds)
    pipe = Popen(cmds, shell=True, stdout=PIPE, stderr=PIPE)
    read_set = [pipe.stderr, pipe.stdout]
    out = err = ""
    try:
        rlist, wlist, xlist = select.select(read_set, [], [], RUN_CMD_TIMEOUT)
        if pipe.stdout in rlist:
            out = pipe.stdout.readlines()
        if pipe.stderr in rlist:
            err = pipe.stderr.readlines()
    except:
        raise
    finally:
        pipe.stdout.close()
        pipe.stderr.close()
    return out, err


def run(cmds: Union[str, list]):
    stdout, stderr = run_command(cmds)
    if stdout:
        return STDOUT, stdout
    if stderr:
        return STDERR, stderr


class STDERRException(Exception):
    pass


async def async_run_shell(cmds: Union[str, list]) -> Tuple[int, bytes]:
    async with async_timeout.timeout(RUN_CMD_TIMEOUT) as tm:
        proc = await asyncio.subprocess.create_subprocess_shell(
            cmds,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return STDOUT, stdout
        if stderr:
            return STDERR, stderr


class FileLock(object):

    def acquire(self, fd):
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def release(self, fd):
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)


class PIDFile(object):

    def __init__(self, pid_file_path):
        self.pid_file = pid_file_path
        self.pid = None
        self.acquired = False

    def open(self):
        self.pid = self._open('a')
        try:
            FileLock().acquire(self.pid.fileno())
        except BlockingIOError:
            self.pid.close()
            self.pid = None
            self.acquired = False
        else:
            self.acquired = True

    def _open(self, mode='r'):
        return open(self.pid_file, mode)

    def write_pid(self):
        pid = os.getpid()
        if self.acquired:
            self.pid.write(str(pid))
            self.pid.flush()

    def read_pid(self):
        with self._open('r') as f:
            read = f.read()
            if read:
                return int(read)
            return

    def remove_pid(self):
        if not os.path.exists(self.pid_file):
            return
        os.remove(self.pid_file)

    def __del__(self):
        self.close()

    def close(self):
        if self.acquired and self.pid:
            try:
                FileLock().release(self.pid)
                self.pid.close()
                self.remove_pid()
            except:
                pass


DECIMAL_SCALE = "DECIMAL"
DECIMAL_UNITS = OrderedDict()
DECIMAL_UNITS.update({
    'byte':  1,
    'K': pow(10, 3),
    'M': pow(10, 6),
    'G': pow(10, 9),
    'T': pow(10, 12),
    'P': pow(10, 15),
    'E': pow(10, 18),
    'Z': pow(10, 21),
    'Y': pow(10, 24),
})

BINARY_SCALE = "BINARY"
BINARY_UNITS = OrderedDict()
BINARY_UNITS.update({
    'KiB': pow(2, 10),
    'MiB': pow(2, 20),
    'GiB': pow(2, 30),
    'TiB': pow(2, 40),
    'PiB': pow(2, 50),
    'EiB': pow(2, 60),
    'ZiB': pow(2, 70),
    'YiB': pow(2, 80),
})

UNITS = {
    DECIMAL_SCALE: DECIMAL_UNITS,
    BINARY_SCALE: BINARY_UNITS
}


def get_standard_unit_name(unit_dict, unit_name):
    _unit_name = None
    for k, v in unit_dict.items():
        if k.lower() == unit_name.lower():
            _unit_name = k
            break
    return _unit_name

def convert_traffic_from_byte(b: int, to_unit: Optional[str]=None,
                          scale: str=DECIMAL_SCALE,
                          force_conver: bool=False) -> str:
    _unit = None
    _scale = None
    _scale_dic = None
    _ndigits = 0

    if scale not in UNITS.keys():
        raise ValueError("Invalid scale")

    if force_conver and not to_unit:
        raise ValueError(
            "'to_unit' must be a string of type when 'force_conver' is true"
        )

    if not to_unit:
        _scale_dic = UNITS[scale]
    else:
        filter_dic = list(filter(
            lambda d: to_unit.lower() in [i.lower() for i in d.keys()],
            list(UNITS.values())))
        if not filter_dic:
            raise ValueError("Invalie unit {}".format(to_unit))
        _scale_dic = filter_dic[0]
        _unit = get_standard_unit_name(_scale_dic, to_unit)

    if _unit:
        if b > _scale_dic[_unit]:
            _ndigits = 2
            _scale = _scale_dic[_unit]
        else:
            if not force_conver:
                _unit = None

    if not _unit and not _scale:
        _ndigits = 2
        ReverseScales = list(_scale_dic.items())
        ReverseScales.reverse()
        for unit, sc in ReverseScales:
            if b >= sc:
                _unit = unit
                _scale = sc
                break
        if not _scale:
            _unit, _scale = ReverseScales[-1]

    if force_conver:
        _ndigits = 2
        _unit = get_standard_unit_name(_scale_dic, to_unit)
        _scale = _scale_dic[_unit]
        keys = list(_scale_dic.keys())
        idx = keys.index(_unit)
        if idx > 1:
            for i in range(idx + 1):
                if b < _scale_dic[keys[idx - 1]]:
                    _ndigits += 2
                else:
                    break
        else:
            _ndigits = 4

    return "{} {}".format(float(round(b / _scale, _ndigits)), _unit)

def convert_traffic_to_byte(t):
    if isinstance(t, float) or isinstance(t, int):
        return t
    import re
    serach_size = re.search('\d+', t)
    if not serach_size:
        raise ValueError("Incorrect parameters, "
                         "unable to get any numbers")
    t_size = float(serach_size.group())
    serach_unit = re.search('[a-zA-Z]+', t)
    if not serach_unit:
        return t_size
    else:
        t_unit = serach_unit.group()

    filter_dic = list(filter(
        lambda d: t_unit.lower() in [i.lower() for i in d.keys()],
        list(UNITS.values())))
    if not filter_dic:
        raise ValueError("Invalie unit {}".format(t_unit))
    _scale_dic = filter_dic[0]
    _unit = get_standard_unit_name(_scale_dic, t_unit)
    return t_size * _scale_dic[_unit]


def import_object(name: str) -> Any:

    if name.count('.') == 0:
        return __import__(name)

    parts = name.split(".")
    obj = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])



class Configurable(object):
    """Base class for configurable interfaces.

    Configurable subclasses must define the class methods
    `configurable_base` and `configurable_default`, and use the instance
    method `initialize` instead of ``__init__``.

    """

    __impl_class = None    # type: Optional[Type[Configurable]]
    __impl_kwargs = None   # type: Dict[str, Any]
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        base = cls.configurable_base()
        init_kwargs = {}  # type: Dict[str, Any]
        if cls is base:
            impl = cls.configurable_class()
            if base.__impl_kwargs:
                init_kwargs.update(base.__impl_kwargs)
        else:
            impl = cls
        init_kwargs.update(kwargs)
        if impl.configurable_base() is not base:
            # The impl class is itself configurable, so recurse.
            return impl(*args, **init_kwargs)
        instance = super(Configurable, cls).__new__(impl)
        instance.initialize(*args, **init_kwargs)
        return instance

    def _initialize(self) -> None:
        pass
    initialize = _initialize  # type: Callable[..., None]

    @classmethod
    def configure(cls, impl, **kwargs):
        base = cls.configurable_base()
        if isinstance(impl, str):
            impl = typing.cast(Type[Configurable], import_object(impl))
        if impl is not None and not issubclass(impl, cls):
            raise ValueError("Invalid subclass of %s" % cls)
        base.__impl_class = impl
        base.__impl_kwargs = kwargs


    @classmethod
    def configurable_base(cls):
        # type: () -> Type[Configurable]
        raise NotImplementedError()

    @classmethod
    def configurable_default(cls):
        # type: () -> Type[Configurable]
        raise NotImplementedError()

    @classmethod
    def configurable_class(cls):
        # type: () -> Type[Configurable]
        base = cls.configurable_base()
        if base.__dict__.get("_Configurable__impl_class") is None:
            base.__impl_class = cls.configurable_default()

        if base.__impl_class is not None:
            return base.__impl_class
        else:
            return ValueError("configured class not found")

    @classmethod
    def _save_configuration(cls):
        # type: () -> Tuple[Optional[Type[Configurable]], Dict[str, Any]]
        base = cls.configurable_base()
        return (base.__impl_class, base.__impl_kwargs)

    @classmethod
    def _restore_configuration(cls, saved):
        # type: (Tuple[Optional[Type[Configurable]], Dict[str, Any]]) -> None
        base = cls.configurable_base()
        base.__impl_class = saved[0]
        base.__impl_kwargs = saved[1]


IPv4Type = TypeVar("IPv4Type", str, int)
import ipaddress
PackIp = lambda x: str(ipaddress.ip_address(x)) if isinstance(x, int) else x

def errno_from_exception(e: BaseException) -> Optional[int]:
    """Provides the errno from an Exception object.

    There are cases that the errno attribute was not set so we pull
    the errno out of the args but if someone instantiates an Exception
    without any args you will get a tuple error. So this function
    abstracts all that behavior to give you a safe way to get the
    errno.
    """

    if hasattr(e, "errno"):
        return e.errno  # type: ignore
    elif e.args:
        return e.args[0]
    else:
        return None

def raise_exc_info(
    exc_info,  # type: Tuple[Optional[type], Optional[BaseException], Optional[TracebackType]]
):
    try:
        if exc_info[1] is not None:
            raise exc_info[1].with_traceback(exc_info[2])
        else:
            raise TypeError("raise_exc_info called with no exeption")
    finally:
        exc_info = (None, None, None)


def print_exception(e):
    global verbose
    if verbose > 0:
        import traceback
        traceback.print_exc()

def record_exception_to_logger(logger=None):
    if not logger:
        from lib.log import logger

    import sys, traceback
    exc_type, exc_value, exc_trace = sys.exc_info()
    logger.error(
        "exception type : {type}, value: {value}".format(
            type=exc_type, value=exc_value
        )
    )
    logger.error(
        "Following is the exception tracking information"
    )
    for trace in traceback.extract_tb(exc_trace):
        logger.error("{}".format(trace))

def is_email(email):
    email_pattern = re.compile(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    if email_pattern.match(email):
        return True
    return False

def to_timestamp_seconds(time, to_datetime=False):

    try:
        time = int(time)
    except (ValueError, TypeError):
        pass

    if isinstance(time, int):
        ts_len = len(str(time))
        assert ts_len >= 10
        if ts_len == 10:
            _time = time
        elif ts_len == 13:
            _time = time / 1000
        elif ts_len == 16:
            _time = time / 1000000
        elif ts_len == 19:
            _time = time / 1000000000
        else:
            raise ValueError("the time is not a valided timestamp")
        if to_datetime:
            return datetime.datetime.fromtimestamp(_time)
        return _time
    if isinstance(time, str):
        try:
            from dateutil.parser import parse as parse_date
            from dateutil.parser import ParserError
        except ImportError:
            raise ImportError(
                "Unable to import dateutil, please run pip install dateutil before use"
            )
        try:
            _time = parse_date(time)
        except (ParserError, OverflowError) as e:
            raise ValueError("the time is not valided time string: %s " % e)
        if to_datetime:
            return _time
        return _time.timestamp()
    raise ValueError("Unknown type")