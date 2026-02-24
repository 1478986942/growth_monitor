import React, { useEffect, useState } from 'react'
import { Table, Button, Modal, Form, Input, message, Space, Popconfirm, Tag } from 'antd'
import { PlusOutlined, DeleteOutlined, UserOutlined } from '@ant-design/icons'
import api from '../services/api'

const Admin = () => {
  const [doctors, setDoctors] = useState([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchDoctors()
  }, [])

  const fetchDoctors = async () => {
    setLoading(true)
    try {
      const response = await api.get('/auth/doctors')
      setDoctors(response.data.doctors)
    } catch (error) {
      message.error(error.response?.data?.error || '获取医生列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    form.resetFields()
    setModalVisible(true)
  }

  const handleSubmit = async (values) => {
    try {
      await api.post('/auth/register-doctor', values)
      message.success('医生添加成功')
      setModalVisible(false)
      fetchDoctors()
    } catch (error) {
      message.error(error.response?.data?.error || '添加失败')
    }
  }

  const handleDelete = async (doctorId) => {
    try {
      await api.delete(`/auth/doctors/${doctorId}`)
      message.success('删除成功')
      fetchDoctors()
    } catch (error) {
      message.error(error.response?.data?.error || '删除失败')
    }
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id'
    },
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username'
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
      render: (email) => email || '-'
    },
    {
      title: '手机号',
      dataIndex: 'phone',
      key: 'phone',
      render: (phone) => phone || '-'
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (role) => <Tag color="blue">{role === 'doctor' ? '医生' : role}</Tag>
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at'
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Popconfirm
            title="确定要删除该医生吗？"
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
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ color: '#3f51b5', margin: 0 }}>医生管理</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加医生
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={doctors}
        rowKey="id"
        loading={loading}
      />
      <Modal
        title="添加医生"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form form={form} onFinish={handleSubmit} layout="vertical">
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="用户名" />
          </Form.Item>
          <Form.Item
            name="email"
            label="邮箱"
            rules={[{ type: 'email', message: '请输入有效的邮箱地址' }]}
          >
            <Input placeholder="邮箱（可选）" />
          </Form.Item>
          <Form.Item
            name="phone"
            label="手机号"
            rules={[{ pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }]}
          >
            <Input placeholder="手机号（可选）" />
          </Form.Item>
          <Form.Item
            name="password"
            label="密码"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password placeholder="密码" />
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

export default Admin
