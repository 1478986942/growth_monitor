import React, { useEffect, useState } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Popconfirm, Space } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Option } = Select

const Children = () => {
  const [children, setChildren] = useState([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingChild, setEditingChild] = useState(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchChildren()
  }, [])

  const fetchChildren = async () => {
    setLoading(true)
    try {
      const response = await api.get('/children')
      setChildren(response.data.children)
    } catch (error) {
      message.error('获取儿童列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingChild(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (record) => {
    setEditingChild(record)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/children/${id}`)
      message.success('删除成功')
      fetchChildren()
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleSubmit = async (values) => {
    try {
      if (editingChild) {
        await api.put(`/children/${editingChild.id}`, values)
        message.success('更新成功')
      } else {
        await api.post('/children', values)
        message.success('添加成功')
      }
      setModalVisible(false)
      fetchChildren()
    } catch (error) {
      message.error(error.response?.data?.error || '操作失败')
    }
  }

  const columns = [
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '性别',
      dataIndex: 'gender',
      key: 'gender',
      render: (gender) => gender === 'male' ? '男' : '女'
    },
    {
      title: '出生日期',
      dataIndex: 'birth_date',
      key: 'birth_date'
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Popconfirm
            title="确定要删除吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h1>儿童管理</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加儿童
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={children}
        rowKey="id"
        loading={loading}
      />
      <Modal
        title={editingChild ? '编辑儿童' : '添加儿童'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form form={form} onFinish={handleSubmit} layout="vertical">
          <Form.Item
            name="name"
            label="姓名"
            rules={[{ required: true, message: '请输入姓名' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="gender"
            label="性别"
            rules={[{ required: true, message: '请选择性别' }]}
          >
            <Select>
              <Option value="male">男</Option>
              <Option value="female">女</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="birth_date"
            label="出生日期"
            rules={[{ required: true, message: '请选择出生日期' }]}
          >
            <Input type="date" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              确定
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Children
