import { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";
// import './dashboard.css';

interface Log {
  input: string;
  response: string;
  status: string;
  timestamp: string;
}

interface Alert {
  type: string;
  input: string;
  timestamp: string;
}

const Dashboard = () => {
  const [logs, setLogs] = useState<Log[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const logsRes = await axios.get("https://d722-96-63-208-24.ngrok-free.app/logs");
      setLogs(logsRes.data);

      const alertsRes = await axios.get("https://d722-96-63-208-24.ngrok-free.app/alerts");
      setAlerts(alertsRes.data);
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">SIEM Dashboard</h1>

      {/* Performance Metrics */}
      <LineChart width={600} height={300} data={logs}>
        <Line type="monotone" dataKey="status" stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
      </LineChart>

      {/* Security Alerts */}
      <div className="mt-6">
        <h2 className="text-lg font-semibold">Security Alerts</h2>
        {alerts.map((alert, idx) => (
          <div key={idx} className="p-2 bg-red-100 border-l-4 border-red-500 mb-2">
            <strong>{alert.type}</strong> at {alert.timestamp}
            <p className="text-sm text-gray-600">{alert.input}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;