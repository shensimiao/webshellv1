<template background: var(--el-color-primary-light-9);>
  <el-row>
    <el-col :span="10">
<div class="scrollbar-demo-item" >
    <div class="mt-4">
      <el-input
                v-model="input3"
                placeholder="Please input"
                class="input-with-select"
                >
        <template #prepend>
          <el-select v-model="select" placeholder="Select" style="width: 115px">
            <el-option label="Restaurant" value="1" />
            <el-option label="Order No." value="2" />
            <el-option label="Tel" value="3" />
          </el-select>
        </template>
        <template #append>
          <el-button :icon="Search" />
        </template>
      </el-input>
    </div>

      </div>
      </el-col>
     <el-col :span="14">
       <div class="scrollbar-demo-item" >
           <el-input
            v-model="text"
            maxlength="20"
            placeholder="IP Prefix"
            show-word-limit
            type="text"
          />
            <el-input
            v-model="text"
            maxlength="20"
            placeholder="Net Mark"
            show-word-limit
            type="text"
          />
          
       </div>
    </el-col>
  </el-row>
    <el-row>
      <el-col :span="10">
               <div class="scrollbar-demo-item" >
            <el-tree
      :props="props"
      :load="loadNode"
      lazy
      show-checkbox
      @check-change="handleCheckChange"
    />
                 </div>
         </el-col>
            <el-col :span="14">
               <button class="action_btn" >CMDS</button>
                     <div class="scrollbar-demo-item such" >
              <el-input class="such" v-model="input" placeholder="脚本示例" clearable />
                       </div>
         </el-col>
      </el-row>
      <el-row>
      <el-col :span="10">
               <div class="scrollbar-demo-item" >
            <el-tree
      :props="props"
      :load="loadNode"
      lazy
      show-checkbox
      @check-change="handleCheckChange"
    />
                 </div>
         </el-col>
            <el-col :span="14">
              <button class="action_btn" >Action</button>
                     <div class="scrollbar-demo-item return" >
              <el-input class="return" v-model="input" placeholder="返回内容" clearable />
                       </div>
         </el-col>
      </el-row>
</template>

<style scoped>
  .input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
.scrollbar-demo-item {
  display: flex;
  align-items: baseline;
  height: auto;
  margin: 10px;
  text-align: center;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
  .return{
    height:600px;
  }
  .such{
    height:200px;
  }
  .action_btn{
    height:30px;
    width:60px;
    margin:0 10px;
    background: var(--el-color-primary-light-9);

  }
.el-row {
  margin-bottom: 0;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}
  .el-tree{
    background: var(--el-color-primary-light-9);
  }
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
<script lang="ts" setup>
  import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

import type Node from 'element-plus/es/components/tree/src/model/node'
let count = 1
const input3 = ref('')
const select = ref('')
interface Tree {
  name: string
}

const props = {
  label: 'name',
  children: 'zones',
}

const handleCheckChange = (
  data: Tree,
  checked: boolean,
  indeterminate: boolean
) => {
  console.log(data, checked, indeterminate)
}

const loadNode = (node: Node, resolve: (data: Tree[]) => void) => {
  if (node.level === 0) {
    return resolve([{ name: 'Root1' }, { name: 'Root2' }, { name: 'Root2' }, { name: 'Root2' }, { name: 'Root2' }])
  }
  if (node.level > 3) return resolve([])

  let hasChild = false
  if (node.data.name === 'region1') {
    hasChild = true
  } else if (node.data.name === 'region2') {
    hasChild = false
  } else {
    hasChild = Math.random() > 0.5
  }

  setTimeout(() => {
    let data: Tree[] = []
    if (hasChild) {
      data = [
        {
          name: `zone${count++}`,
        },
        {
          name: `zone${count++}`,
        },
      ]
    } else {
      data = []
    }

    resolve(data)
  }, 500)
}
</script>