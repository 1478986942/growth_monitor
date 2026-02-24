import React, { useEffect, useState } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Popconfirm, Space, Row, Col, Card } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import ReactECharts from 'echarts-for-react'
import api from '../services/api'

const { Option } = Select

const Growth = () => {
  const [children, setChildren] = useState([])
  const [records, setRecords] = useState([])
  const [selectedChild, setSelectedChild] = useState(null)
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingRecord, setEditingRecord] = useState(null)
  const [form] = Form.useForm()
  const navigate = useNavigate()

  useEffect(() => {
    fetchChildren()
  }, [])

  useEffect(() => {
    if (selectedChild) {
      fetchRecords(selectedChild.id)
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

  const fetchRecords = async (childId) => {
    setLoading(true)
    try {
      const response = await api.get(`/growth/child/${childId}`)
      setRecords(response.data.records)
    } catch (error) {
      message.error('获取生长记录失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    if (!selectedChild) {
      message.warning('请先选择儿童')
      return
    }
    setEditingRecord(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (record) => {
    setEditingRecord(record)
    form.setFieldsValue({
      ...record,
      record_date: record.record_date
    })
    setModalVisible(true)
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/growth/${id}`)
      message.success('删除成功')
      fetchRecords(selectedChild.id)
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleSubmit = async (values) => {
    try {
      const data = {
        ...values,
        child_id: selectedChild.id
      }
      if (editingRecord) {
        await api.put(`/growth/${editingRecord.id}`, data)
        message.success('更新成功')
      } else {
        await api.post('/growth', data)
        message.success('添加成功')
      }
      setModalVisible(false)
      fetchRecords(selectedChild.id)
    } catch (error) {
      message.error(error.response?.data?.error || '操作失败')
    }
  }

  const columns = [
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

  const getChartOption = () => {
    const sortedRecords = [...records].sort((a, b) => new Date(a.record_date) - new Date(b.record_date))
    const dates = sortedRecords.map(r => r.record_date)
    const heights = sortedRecords.map(r => r.height)
    const weights = sortedRecords.map(r => r.weight)
    const bmis = sortedRecords.map(r => r.bmi)

    return {
      title: {
        text: selectedChild ? `${selectedChild.name} 生长趋势图` : '生长趋势图',
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#3f51b5'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['身高', '体重', 'BMI'],
        top: 30
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: dates,
        name: '日期',
        nameLocation: 'middle',
        nameGap: 30
      },
      yAxis: [
        {
          type: 'value',
          name: '身高/体重',
          position: 'left',
          axisLabel: {
            formatter: '{value}'
          }
        },
        {
          type: 'value',
          name: 'BMI',
          position: 'right',
          axisLabel: {
            formatter: '{value}'
          }
        }
      ],
      series: [
        {
          name: '身高',
          type: 'line',
          data: heights,
          smooth: true,
          itemStyle: {
            color: '#3f51b5'
          },
          lineStyle: {
            width: 3
          },
          symbol: 'circle',
          symbolSize: 8
        },
        {
          name: '体重',
          type: 'line',
          data: weights,
          smooth: true,
          itemStyle: {
            color: '#ff9800'
          },
          lineStyle: {
            width: 3
          },
          symbol: 'circle',
          symbolSize: 8
        },
        {
          name: 'BMI',
          type: 'line',
          yAxisIndex: 1,
          data: bmis,
          smooth: true,
          itemStyle: {
            color: '#4caf50'
          },
          lineStyle: {
            width: 3
          },
          symbol: 'circle',
          symbolSize: 8
        }
      ]
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
          <Space>
            <Button onClick={() => navigate('/risk')} disabled={!selectedChild}>
              风险评估
            </Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd} disabled={!selectedChild}>
              添加数据
            </Button>
          </Space>
        </Col>
      </Row>
      
      {records.length > 0 && (
        <Card style={{ marginBottom: 16 }}>
          <ReactECharts option={getChartOption()} style={{ height: '400px' }} />
        </Card>
      )}
      
      <Table
        columns={columns}
        dataSource={records}
        rowKey="id"
        loading={loading}
      />
      <Modal
        title={editingRecord ? '编辑生长记录' : '添加生长记录'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form form={form} onFinish={handleSubmit} layout="vertical">
          <Form.Item
            name="record_date"
            label="测量日期"
            rules={[{ required: true, message: '请选择测量日期' }]}
          >
            <Input type="date" />
          </Form.Item>
          <Form.Item
            name="height"
            label="身高"
            rules={[{ required: true, message: '请输入身高' }]}
          >
            <Input type="number" step="0.1" suffix="cm" />
          </Form.Item>
          <Form.Item
            name="weight"
            label="体重"
            rules={[{ required: true, message: '请输入体重' }]}
          >
            <Input type="number" step="0.1" suffix="kg" />
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

export default Growth
