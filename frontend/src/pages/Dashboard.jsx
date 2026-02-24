import React, { useEffect, useState } from 'react'
import { Card, Row, Col, Statistic, message } from 'antd'
import { UserOutlined, BarChartOutlined, SafetyOutlined, MedicineBoxOutlined } from '@ant-design/icons'
import api from '../services/api'

const Dashboard = () => {
  const [stats, setStats] = useState({
    children: 0,
    records: 0,
    assessments: 0,
    interventions: 0
  })

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const [childrenRes, recordsRes, assessmentsRes, interventionsRes] = await Promise.all([
        api.get('/children'),
        api.get('/growth/records'),
        api.get('/risk/assessments'),
        api.get('/intervention/interventions')
      ])

      setStats({
        children: childrenRes.data.children?.length || 0,
        records: recordsRes.data.records?.length || 0,
        assessments: assessmentsRes.data.assessments?.length || 0,
        interventions: interventionsRes.data.interventions?.length || 0
      })
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  return (
    <div>
      <h1 style={{ color: '#3f51b5', marginBottom: 24 }}>仪表盘</h1>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={6}>
          <Card style={{ background: 'linear-gradient(135deg, #5c6bc0 0%, #3f51b5 100%)', color: '#fff' }}>
            <Statistic
              title="儿童数量"
              value={stats.children}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#fff' }}
              titleStyle={{ color: '#fff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card style={{ background: 'linear-gradient(135deg, #7986cb 0%, #5c6bc0 100%)', color: '#fff' }}>
            <Statistic
              title="生长记录"
              value={stats.records}
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#fff' }}
              titleStyle={{ color: '#fff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card style={{ background: 'linear-gradient(135deg, #9fa8da 0%, #7986cb 100%)', color: '#fff' }}>
            <Statistic
              title="风险评估"
              value={stats.assessments}
              prefix={<SafetyOutlined />}
              valueStyle={{ color: '#fff' }}
              titleStyle={{ color: '#fff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card style={{ background: 'linear-gradient(135deg, #c5cae9 0%, #9fa8da 100%)', color: '#fff' }}>
            <Statistic
              title="干预方案"
              value={stats.interventions}
              prefix={<MedicineBoxOutlined />}
              valueStyle={{ color: '#fff' }}
              titleStyle={{ color: '#fff' }}
            />
          </Card>
        </Col>
      </Row>
      <Card style={{ marginTop: 24, background: 'linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%)' }}>
        <h2 style={{ color: '#3f51b5' }}>欢迎使用儿童生长发育智能监测与干预平台</h2>
        <p style={{ marginTop: 16, lineHeight: 1.8, color: '#5c6bc0' }}>
          本平台旨在帮助家长监测儿童生长发育情况，识别潜在风险，并提供个性化干预方案。
          通过AI整合生长数据，识别矮小症、肥胖等风险，提供个性化干预方案与就医绿色通道，
          早期干预价值明确，还可延伸对接母婴、儿科医疗产业链资源。
        </p>
      </Card>
    </div>
  )
}

export default Dashboard
