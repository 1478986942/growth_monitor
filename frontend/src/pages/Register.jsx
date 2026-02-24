import React, { useState } from 'react'
import { Form, Input, Button, Card, message } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined, PhoneOutlined, SafetyOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const Register = () => {
  const [loading, setLoading] = useState(false)
  const [sendingCode, setSendingCode] = useState(false)
  const [countdown, setCountdown] = useState(0)
  const navigate = useNavigate()
  const [form] = Form.useForm()

  const sendVerificationCode = async () => {
    const email = form.getFieldValue('email')
    if (!email) {
      message.warning('请先输入邮箱地址')
      return
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      message.warning('请输入有效的邮箱地址')
      return
    }
    
    setSendingCode(true)
    try {
      await api.post('/auth/send-verification-code', { email })
      message.success('验证码已发送到您的邮箱')
      setCountdown(60)
      const timer = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(timer)
            return 0
          }
          return prev - 1
        })
      }, 1000)
    } catch (error) {
      message.error(error.response?.data?.error || '发送验证码失败')
    } finally {
      setSendingCode(false)
    }
  }

  const onFinish = async (values) => {
    setLoading(true)
    try {
      const response = await api.post('/auth/register', values)
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      message.success('注册成功')
      navigate('/dashboard')
    } catch (error) {
      message.error(error.response?.data?.error || '注册失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: 'linear-gradient(135deg, #3f51b5 0%, #673ab7 100%)' }}>
      <Card title="注册" style={{ width: 400, boxShadow: '0 4px 12px rgba(63, 81, 181, 0.3)' }}>
        <Form form={form} name="register" onFinish={onFinish} autoComplete="off">
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="用户名" size="large" />
          </Form.Item>
          <Form.Item
            name="email"
            rules={[
              { required: true, message: '请输入邮箱地址' },
              { type: 'email', message: '请输入有效的邮箱地址' }
            ]}
          >
            <Input prefix={<MailOutlined />} placeholder="邮箱" size="large" />
          </Form.Item>
          <Form.Item>
            <div style={{ display: 'flex', gap: '8px' }}>
              <Form.Item
                name="verification_code"
                noStyle
                rules={[{ required: true, message: '请输入验证码' }]}
              >
                <Input prefix={<SafetyOutlined />} placeholder="验证码" size="large" style={{ flex: 1 }} />
              </Form.Item>
              <Button 
                type="primary" 
                onClick={sendVerificationCode} 
                loading={sendingCode}
                disabled={countdown > 0}
                size="large"
              >
                {countdown > 0 ? `${countdown}秒后重发` : '发送验证码'}
              </Button>
            </div>
          </Form.Item>
          <Form.Item
            name="phone"
            rules={[{ pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }]}
          >
            <Input prefix={<PhoneOutlined />} placeholder="手机号(可选)" size="large" />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="密码" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block size="large">
              注册
            </Button>
          </Form.Item>
          <div style={{ textAlign: 'center' }}>
            已有账号？<a onClick={() => navigate('/login')}>立即登录</a>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default Register