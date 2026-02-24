import React, { useEffect, useState } from 'react'
import { Card, List, Tag, message, Row, Col, Input, Space } from 'antd'
import { BankOutlined, PhoneOutlined, EnvironmentOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Search } = Input

const Hospital = () => {
  const [hospitals, setHospitals] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchText, setSearchText] = useState('')

  useEffect(() => {
    fetchHospitals()
  }, [])

  const fetchHospitals = async () => {
    setLoading(true)
    try {
      const response = await api.get('/hospital')
      setHospitals(response.data.hospitals)
    } catch (error) {
      message.error('获取医院信息失败')
    } finally {
      setLoading(false)
    }
  }

  const filteredHospitals = hospitals.filter(hospital =>
    hospital.name.toLowerCase().includes(searchText.toLowerCase()) ||
    hospital.department?.toLowerCase().includes(searchText.toLowerCase()) ||
    hospital.address?.toLowerCase().includes(searchText.toLowerCase())
  )

  return (
    <div>
      <h1>就医绿色通道</h1>
      <Card style={{ marginBottom: 16 }}>
        <Search
          placeholder="搜索医院名称、科室或地址"
          allowClear
          enterButton
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
      </Card>
      <Row gutter={[16, 16]}>
        {filteredHospitals.map(hospital => (
          <Col xs={24} md={12} lg={8} key={hospital.id}>
            <Card
              title={<><BankOutlined /> {hospital.name}</>}
              extra={<Tag color="blue">合作医院</Tag>}
              hoverable
            >
              <List size="small">
                {hospital.department && (
                  <List.Item>
                    <Space>
                      <BankOutlined />
                      <span>{hospital.department}</span>
                    </Space>
                  </List.Item>
                )}
                {hospital.address && (
                  <List.Item>
                    <Space>
                      <EnvironmentOutlined />
                      <span>{hospital.address}</span>
                    </Space>
                  </List.Item>
                )}
                {hospital.phone && (
                  <List.Item>
                    <Space>
                      <PhoneOutlined />
                      <span>{hospital.phone}</span>
                    </Space>
                  </List.Item>
                )}
              </List>
              {hospital.description && (
                <div style={{ marginTop: 16, color: '#666' }}>
                  {hospital.description}
                </div>
              )}
            </Card>
          </Col>
        ))}
      </Row>
      {filteredHospitals.length === 0 && (
        <Card>
          <p style={{ textAlign: 'center', color: '#999' }}>
            {searchText ? '未找到匹配的医院' : '暂无医院信息'}
          </p>
        </Card>
      )}
    </div>
  )
}

export default Hospital
