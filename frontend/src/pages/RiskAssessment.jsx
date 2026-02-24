import React, { useEffect, useState } from 'react'
import { Card, Button, Select, message, Descriptions, Alert, Space, Row, Col, Progress, Statistic, Table } from 'antd'
import { SafetyOutlined, ThunderboltOutlined, FileTextOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const { Option } = Select

const Risk = () => {
  const [children, setChildren] = useState([])
  const [assessments, setAssessments] = useState([])
  const [growthRecords, setGrowthRecords] = useState([])
  const [selectedChild, setSelectedChild] = useState(null)
  const [loading, setLoading] = useState(false)
  const [assessing, setAssessing] = useState(false)
  const [generating, setGenerating] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchChildren()
  }, [])

  useEffect(() => {
    if (selectedChild) {
      fetchAssessments(selectedChild.id)
      fetchGrowthRecords(selectedChild.id)
    }
  }, [selectedChild])

  const fetchChildren = async () => {
    try {
      const response = await api.get('/children')
      setChildren(response.data.children)
      if (response.data.children.length > 0 && !selectedChild) {
        setSelectedChild(response.data.children[0])
      }
    } catch (error) {
      message.error('获取儿童列表失败')
    }
  }

  const fetchAssessments = async (childId) => {
    setLoading(true)
    try {
      const response = await api.get(`/risk/child/${childId}`)
      setAssessments(response.data.assessments)
    } catch (error) {
      message.error('获取评估记录失败')
    } finally {
      setLoading(false)
    }
  }

  const fetchGrowthRecords = async (childId) => {
    try {
      const response = await api.get(`/growth/child/${childId}`)
      setGrowthRecords(response.data.records || [])
    } catch (error) {
      console.error('获取生长数据失败:', error)
    }
  }

  const handleAssess = async () => {
    if (!selectedChild) {
      message.warning('请先选择儿童')
      return
    }
    setAssessing(true)
    try {
      await api.post(`/risk/assess/${selectedChild.id}`)
      message.success('评估完成')
      fetchAssessments(selectedChild.id)
    } catch (error) {
      message.error(error.response?.data?.error || '评估失败')
    } finally {
      setAssessing(false)
    }
  }

  const handleGenerateIntervention = async () => {
    if (!selectedChild) {
      message.warning('请先选择儿童')
      return
    }
    if (assessments.length === 0) {
      message.warning('请先进行风险评估')
      return
    }
    setGenerating(true)
    try {
      await api.post('/intervention/generate', {
        assessment_id: assessments[0].id
      })
      message.success('干预方案生成成功')
      navigate('/intervention')
    } catch (error) {
      message.error(error.response?.data?.error || '生成失败')
    } finally {
      setGenerating(false)
    }
  }

  const getRiskLevel = (risk) => {
    if (risk >= 70) return { level: '高风险', color: '#cf1322' }
    if (risk >= 40) return { level: '中风险', color: '#faad14' }
    return { level: '低风险', color: '#52c41a' }
  }

  const latestAssessment = assessments.length > 0 ? assessments[0] : null

  const growthColumns = [
    {
      title: '测量日期',
      dataIndex: 'record_date',
      key: 'record_date'
    },
    {
      title: '身高',
      dataIndex: 'height',
      key: 'height',
      render: (height) => height ? `${height} cm` : '-'
    },
    {
      title: '体重',
      dataIndex: 'weight',
      key: 'weight',
      render: (weight) => weight ? `${weight} kg` : '-'
    },
    {
      title: 'BMI',
      dataIndex: 'bmi',
      key: 'bmi',
      render: (bmi) => bmi ? bmi.toFixed(2) : '-'
    }
  ]

  const latestGrowthRecords = growthRecords.slice(0, 5)

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col xs={24} md={8}>
          <Select
            style={{ width: '100%' }}
            placeholder="选择儿童"
            value={selectedChild?.id}
            onChange={(value) => setSelectedChild(children.find(c => c.id === value))}
          >
            {children.map(child => (
              <Option key={child.id} value={child.id}>
                {child.name}
              </Option>
            ))}
          </Select>
        </Col>
        <Col xs={24} md={8} style={{ textAlign: 'right' }}>
          <Button
            type="primary"
            icon={<SafetyOutlined />}
            onClick={handleAssess}
            loading={assessing}
            disabled={!selectedChild}
          >
            开始评估
          </Button>
        </Col>
        <Col xs={24} md={8} style={{ textAlign: 'right' }}>
          <Button
            type="default"
            icon={<FileTextOutlined />}
            onClick={handleGenerateIntervention}
            loading={generating}
            disabled={!selectedChild || assessments.length === 0}
          >
            生成干预方案
          </Button>
        </Col>
      </Row>

      {selectedChild && latestGrowthRecords.length > 0 && (
        <Card title="最近生长数据" style={{ marginBottom: 16 }}>
          <Table
            dataSource={latestGrowthRecords}
            columns={growthColumns}
            rowKey="id"
            pagination={false}
            size="small"
          />
        </Card>
      )}

      {latestAssessment ? (
        <Row gutter={[16, 16]}>
          <Col xs={24} md={12}>
            <Card title="矮小症风险评估" extra={<SafetyOutlined />}>
              <Descriptions column={1}>
                <Descriptions.Item label="风险概率">
                  <Progress
                    percent={latestAssessment.stunting_risk}
                    status={latestAssessment.stunting_risk >= 70 ? 'exception' : latestAssessment.stunting_risk >= 40 ? 'active' : 'success'}
                  />
                </Descriptions.Item>
                <Descriptions.Item label="风险等级">
                  <span style={{ color: getRiskLevel(latestAssessment.stunting_risk).color, fontWeight: 'bold' }}>
                    {getRiskLevel(latestAssessment.stunting_risk).level}
                  </span>
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
          <Col xs={24} md={12}>
            <Card title="肥胖风险评估" extra={<ThunderboltOutlined />}>
              <Descriptions column={1}>
                <Descriptions.Item label="风险概率">
                  <Progress
                    percent={latestAssessment.obesity_risk}
                    status={latestAssessment.obesity_risk >= 70 ? 'exception' : latestAssessment.obesity_risk >= 40 ? 'active' : 'success'}
                  />
                </Descriptions.Item>
                <Descriptions.Item label="风险等级">
                  <span style={{ color: getRiskLevel(latestAssessment.obesity_risk).color, fontWeight: 'bold' }}>
                    {getRiskLevel(latestAssessment.obesity_risk).level}
                  </span>
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
          <Col xs={24}>
            <Card title="详细分析">
              <Alert
                message="评估详情"
                description={
                  <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                    {JSON.stringify(latestAssessment.details, null, 2)}
                  </pre>
                }
                type="info"
              />
            </Card>
          </Col>
        </Row>
      ) : (
        <Card>
          <Alert
            message="暂无评估记录"
            description="请点击「开始评估」按钮进行风险评估"
            type="info"
            showIcon
          />
        </Card>
      )}
    </div>
  )
}

export default Risk
