import React, { useEffect, useState } from 'react'
import { Card, Button, Select, message, Descriptions, Tag, Space, Row, Col, Modal, Form, Input, DatePicker } from 'antd'
import { MedicineBoxOutlined, CheckCircleOutlined, EditOutlined } from '@ant-design/icons'
import api from '../services/api'
import moment from 'moment'

const { Option } = Select

const Intervention = () => {
  const [children, setChildren] = useState([])
  const [interventions, setInterventions] = useState([])
  const [assessments, setAssessments] = useState([])
  const [selectedChild, setSelectedChild] = useState(null)
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [detailModal, setDetailModal] = useState(false)
  const [editModal, setEditModal] = useState(false)
  const [selectedIntervention, setSelectedIntervention] = useState(null)
  const [editForm] = Form.useForm()

  useEffect(() => {
    fetchChildren()
  }, [])

  useEffect(() => {
    if (selectedChild) {
      fetchInterventions(selectedChild.id)
      fetchAssessments(selectedChild.id)
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

  const fetchInterventions = async (childId) => {
    setLoading(true)
    try {
      const response = await api.get(`/intervention/child/${childId}`)
      setInterventions(response.data.interventions)
    } catch (error) {
      message.error('获取干预方案失败')
    } finally {
      setLoading(false)
    }
  }

  const fetchAssessments = async (childId) => {
    try {
      const response = await api.get(`/risk/child/${childId}`)
      setAssessments(response.data.assessments)
    } catch (error) {
      console.error('Failed to fetch assessments:', error)
    }
  }

  const handleGenerate = async () => {
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
      fetchInterventions(selectedChild.id)
    } catch (error) {
      message.error(error.response?.data?.error || '生成失败')
    } finally {
      setGenerating(false)
    }
  }

  const handleStatusChange = async (interventionId, status) => {
    try {
      await api.patch(`/intervention/${interventionId}/status`, { status })
      message.success('状态更新成功')
      fetchInterventions(selectedChild.id)
    } catch (error) {
      message.error('状态更新失败')
    }
  }

  const showDetail = (intervention) => {
    setSelectedIntervention(intervention)
    setDetailModal(true)
  }

  const showEdit = (intervention) => {
    setSelectedIntervention(intervention)
    editForm.setFieldsValue({
      plan_title: intervention.plan_title,
      plan_content: intervention.plan_content,
      start_date: moment(intervention.start_date),
      end_date: moment(intervention.end_date)
    })
    setEditModal(true)
  }

  const handleEdit = async (values) => {
    try {
      const data = {
        ...values,
        start_date: values.start_date.format('YYYY-MM-DD'),
        end_date: values.end_date.format('YYYY-MM-DD')
      }
      await api.put(`/intervention/${selectedIntervention.id}`, data)
      message.success('更新成功')
      setEditModal(false)
      fetchInterventions(selectedChild.id)
    } catch (error) {
      message.error('更新失败')
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'default'
      case 'ongoing': return 'processing'
      case 'completed': return 'success'
      default: return 'default'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'pending': return '待执行'
      case 'ongoing': return '进行中'
      case 'completed': return '已完成'
      default: return status
    }
  }

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
        <Col xs={24} md={16} style={{ textAlign: 'right' }}>
          <Button
            type="primary"
            icon={<MedicineBoxOutlined />}
            onClick={handleGenerate}
            loading={generating}
            disabled={!selectedChild || assessments.length === 0}
          >
            生成干预方案
          </Button>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        {interventions.map(intervention => (
          <Col xs={24} md={12} key={intervention.id}>
            <Card
              title={intervention.plan_title}
              extra={
                <Space>
                  <Tag color={getStatusColor(intervention.status)}>{getStatusText(intervention.status)}</Tag>
                  <Button type="link" size="small" onClick={() => showDetail(intervention)}>
                    查看详情
                  </Button>
                  <Button type="link" size="small" icon={<EditOutlined />} onClick={() => showEdit(intervention)}>
                    编辑
                  </Button>
                </Space>
              }
            >
              <Descriptions column={1} size="small">
                <Descriptions.Item label="开始日期">{intervention.start_date}</Descriptions.Item>
                <Descriptions.Item label="结束日期">{intervention.end_date}</Descriptions.Item>
              </Descriptions>
              <Space style={{ marginTop: 16 }}>
                {intervention.status === 'pending' && (
                  <Button size="small" type="primary" onClick={() => handleStatusChange(intervention.id, 'ongoing')}>
                    开始执行
                  </Button>
                )}
                {intervention.status === 'ongoing' && (
                  <Button size="small" type="primary" icon={<CheckCircleOutlined />} onClick={() => handleStatusChange(intervention.id, 'completed')}>
                    标记完成
                  </Button>
                )}
              </Space>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal
        title="干预方案详情"
        open={detailModal}
        onCancel={() => setDetailModal(false)}
        footer={null}
        width={800}
      >
        {selectedIntervention && (
          <div>
            <Descriptions column={2} bordered>
              <Descriptions.Item label="方案标题" span={2}>{selectedIntervention.plan_title}</Descriptions.Item>
              <Descriptions.Item label="开始日期">{selectedIntervention.start_date}</Descriptions.Item>
              <Descriptions.Item label="结束日期">{selectedIntervention.end_date}</Descriptions.Item>
              <Descriptions.Item label="状态" span={2}>
                <Tag color={getStatusColor(selectedIntervention.status)}>{getStatusText(selectedIntervention.status)}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="方案内容" span={2}>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                  {selectedIntervention.plan_content}
                </pre>
              </Descriptions.Item>
            </Descriptions>
          </div>
        )}
      </Modal>

      <Modal
        title="编辑干预方案"
        open={editModal}
        onCancel={() => setEditModal(false)}
        footer={null}
        width={800}
      >
        <Form form={editForm} onFinish={handleEdit} layout="vertical">
          <Form.Item
            name="plan_title"
            label="方案标题"
            rules={[{ required: true, message: '请输入方案标题' }]}
          >
            <Input placeholder="请输入方案标题" />
          </Form.Item>
          <Form.Item
            name="start_date"
            label="开始日期"
            rules={[{ required: true, message: '请选择开始日期' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="end_date"
            label="结束日期"
            rules={[{ required: true, message: '请选择结束日期' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item
            name="plan_content"
            label="方案内容"
            rules={[{ required: true, message: '请输入方案内容' }]}
          >
            <Input.TextArea rows={10} placeholder="请输入方案内容" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              保存
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Intervention
