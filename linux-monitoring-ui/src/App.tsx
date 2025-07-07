import { useEffect, useState } from 'react'
import axios from 'axios'

function App() {
  interface MetricsData {
    cpu: {
      cpu_percent: number;
      cpu_count: number;
      cpu_freq: { current: number };
    };
    memory: {
      used: number;
      total: number;
      percent: number;
    };
    disk: {
      used: number;
      total: number;
      percent: number;
    };
    system: {
      platform: string;
      platform_version: string;
      architecture: string;
      uptime: string;
    };
  }

  const [data, setData] = useState<MetricsData | null>(null)

  useEffect(() => {
    axios.get('http://localhost:8000/metrics')
      .then(res => setData(res.data))
      .catch(err => console.error(err))
  }, [])

  if (!data) return <div className="text-center mt-10 text-xl">Loading...</div>

  const Card = ({ title, children }) => (
    <div className="p-4 bg-white rounded-2xl shadow-md w-full max-w-md">
      <h2 className="text-xl font-semibold mb-2">{title}</h2>
      <div className="text-sm">{children}</div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center gap-6">
      <h1 className="text-3xl font-bold">System Metrics Dashboard</h1>

      <Card title="CPU Info">
        <p><strong>Usage:</strong> {data.cpu.cpu_percent}%</p>
        <p><strong>Cores:</strong> {data.cpu.cpu_count}</p>
        <p><strong>Frequency:</strong> {data.cpu.cpu_freq.current} MHz</p>
      </Card>

      <Card title="Memory Info">
        <p><strong>Used:</strong> {(data.memory.used / 1e9).toFixed(2)} GB</p>
        <p><strong>Total:</strong> {(data.memory.total / 1e9).toFixed(2)} GB</p>
        <p><strong>Usage:</strong> {data.memory.percent}%</p>
      </Card>

      <Card title="Disk Info">
        <p><strong>Used:</strong> {(data.disk.used / 1e9).toFixed(2)} GB</p>
        <p><strong>Total:</strong> {(data.disk.total / 1e9).toFixed(2)} GB</p>
        <p><strong>Usage:</strong> {data.disk.percent}%</p>
      </Card>

      <Card title="System Info">
        <p><strong>Platform:</strong> {data.system.platform}</p>
        <p><strong>Version:</strong> {data.system.platform_version}</p>
        <p><strong>Architecture:</strong> {data.system.architecture}</p>
        <p><strong>Uptime:</strong> {data.system.uptime}</p>
      </Card>
    </div>
  )
}

export default App
