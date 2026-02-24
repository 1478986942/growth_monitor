import React, { useState } from 'react'
import { Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import {
  UserOutlined,
  BarChartOutlined,
  SafetyOutlined,
  MedicineBoxOutlined,
  BankOutlined,
  BookOutlined,
  LogoutOutlined,
  TeamOutlined
} from '@ant-design/icons'

const { Header, Sider, Content } = Layout

import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Children from './pages/Children'
import GrowthRecords from './pages/GrowthRecords'
import RiskAssessment from './pages/RiskAssessment'
import Interventions from './pages/Interventions'
import Hospitals from './pages/Hospitals'
import Resources from './pages/Resources'
import Admin from './pages/Admin'
import PrivateRoute from './components/PrivateRoute'
import { AuthProvider, useAuth } from './contexts/AuthContext'

function AppContent() {
  const [collapsed, setCollapsed] = useState(false)
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const parentMenuItems = [
    {
      key: '/dashboard',
      icon: <BarChartOutlined />,
      label: '仪表盘'
    },
    {
      key: '/children',
      icon: <UserOutlined />,
      label: '儿童管理'
    },
    {
      key: '/growth',
      icon: <BarChartOutlined />,
      label: '生长数据'
    },
    {
      key: '/risk',
      icon: <SafetyOutlined />,
      label: '风险评估'
    },
    {
      key: '/intervention',
      icon: <MedicineBoxOutlined />,
      label: '干预方案'
    },
    {
      key: '/hospital',
      icon: <BankOutlined />,
      label: '就医绿色通道'
    },
    {
      key: '/resources',
      icon: <BookOutlined />,
      label: '资源中心'
    }
  ]

  const adminMenuItems = [
    {
      key: '/dashboard',
      icon: <BarChartOutlined />,
      label: '仪表盘'
    },
    {
      key: '/admin',
      icon: <TeamOutlined />,
      label: '医生管理'
    },
    {
      key: '/resources',
      icon: <BookOutlined />,
      label: '资源中心'
    }
  ]

  const menuItems = user?.role === 'admin' ? adminMenuItems : parentMenuItems

  const handleMenuClick = ({ key }) => {
    navigate(key)
  }

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  const MainLayout = ({ children }) => (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: collapsed ? 16 : 20, fontWeight: 'bold' }}>
          {collapsed ? 'LOG' : 'Lighthouse'}
        </div>
        <Menu
          theme="dark"
          selectedKeys={[location.pathname]}
          mode="inline"
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout>
        <Header style={{ background: 'linear-gradient(90deg, #3f51b5 0%, #5c6bc0 100%)', padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 2px 8px rgba(63, 81, 181, 0.3)' }}>
          <h2 style={{ margin: 0, color: '#fff' }}>儿童生长发育智能监测与干预平台</h2>
          <Menu
            theme="light"
            mode="horizontal"
            items={[
              {
                key: 'logout',
                icon: <LogoutOutlined />,
                label: '退出登录',
                onClick: handleLogout
              }
            ]}
          />
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: '#e8eaf6', borderRadius: 8 }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  )

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/*"
        element={
          <PrivateRoute>
            <MainLayout>
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/children" element={<Children />} />
                <Route path="/growth" element={<GrowthRecords />} />
                <Route path="/risk" element={<RiskAssessment />} />
                <Route path="/intervention" element={<Interventions />} />
                <Route path="/hospital" element={<Hospitals />} />
                <Route path="/resources" element={<Resources />} />
                <Route path="/admin" element={<Admin />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </MainLayout>
          </PrivateRoute>
        }
      />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
