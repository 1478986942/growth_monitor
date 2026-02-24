import React, { useEffect, useState } from 'react'
import { Card, List, Tag, message, Row, Col, Tabs } from 'antd'
import { BookOutlined, LinkOutlined, CoffeeOutlined, LineChartOutlined, HeartOutlined, SmileOutlined, UserOutlined, MedicineBoxOutlined, AlertOutlined, TrophyOutlined } from '@ant-design/icons'
import api from '../services/api'

const Resources = () => {
  const [resources, setResources] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchResources()
  }, [])

  const fetchResources = async () => {
    setLoading(true)
    try {
      const response = await api.get('/resource')
      setResources(response.data.resources)
    } catch (error) {
      message.error('获取资源失败')
    } finally {
      setLoading(false)
    }
  }

  const getCategoryInfo = (category) => {
    const categoryMap = {
      nutrition: { name: '营养饮食', color: 'green', icon: <CoffeeOutlined /> },
      growth: { name: '生长发育', color: 'blue', icon: <LineChartOutlined /> },
      health: { name: '健康保健', color: 'red', icon: <HeartOutlined /> },
      psychology: { name: '心理健康', color: 'purple', icon: <SmileOutlined /> },
      parenting: { name: '育儿指导', color: 'orange', icon: <UserOutlined /> },
      medical: { name: '医疗知识', color: 'cyan', icon: <MedicineBoxOutlined /> },
      emergency: { name: '急救指南', color: 'volcano', icon: <AlertOutlined /> },
      development: { name: '能力发展', color: 'gold', icon: <TrophyOutlined /> }
    }
    return categoryMap[category] || { name: '其他', color: 'default', icon: <BookOutlined /> }
  }

  const getCategoryResources = (category) => {
    return resources.filter(r => r.category === category)
  }

  const renderResourceList = (resourceList) => (
    <List
      grid={{ gutter: 16, xs: 1, sm: 2, md: 2, lg: 3 }}
      dataSource={resourceList}
      renderItem={item => {
        const categoryInfo = getCategoryInfo(item.category)
        return (
          <List.Item>
            <Card
              title={<>{categoryInfo.icon} {item.title}</>}
              extra={<Tag color={categoryInfo.color}>{categoryInfo.name}</Tag>}
              hoverable
            >
              <div style={{ minHeight: 100, marginBottom: 16, lineHeight: 1.5 }}>
                {item.content}
              </div>
              {item.link && (
                <a href={item.link} target="_blank" rel="noopener noreferrer">
                  <LinkOutlined /> 查看详情
                </a>
              )}
            </Card>
          </List.Item>
        )
      }}
    />
  )

  const tabItems = [
    {
      key: 'all',
      label: '全部资源',
      children: renderResourceList(resources)
    },
    {
      key: 'nutrition',
      label: '营养饮食',
      children: renderResourceList(getCategoryResources('nutrition'))
    },
    {
      key: 'growth',
      label: '生长发育',
      children: renderResourceList(getCategoryResources('growth'))
    },
    {
      key: 'health',
      label: '健康保健',
      children: renderResourceList(getCategoryResources('health'))
    },
    {
      key: 'psychology',
      label: '心理健康',
      children: renderResourceList(getCategoryResources('psychology'))
    },
    {
      key: 'parenting',
      label: '育儿指导',
      children: renderResourceList(getCategoryResources('parenting'))
    },
    {
      key: 'medical',
      label: '医疗知识',
      children: renderResourceList(getCategoryResources('medical'))
    },
    {
      key: 'emergency',
      label: '急救指南',
      children: renderResourceList(getCategoryResources('emergency'))
    },
    {
      key: 'development',
      label: '能力发展',
      children: renderResourceList(getCategoryResources('development'))
    }
  ]

  return (
    <div>
      <h1 style={{ color: '#3f51b5', marginBottom: 24 }}>资源中心</h1>
      <Card loading={loading}>
        <Tabs 
          items={tabItems} 
          tabPosition="left"
          style={{ minHeight: 600 }}
        />
      </Card>
      {resources.length === 0 && !loading && (
        <Card style={{ marginTop: 16 }}>
          <p style={{ textAlign: 'center', color: '#999' }}>
            暂无资源信息
          </p>
        </Card>
      )}
    </div>
  )
}

export default Resources
