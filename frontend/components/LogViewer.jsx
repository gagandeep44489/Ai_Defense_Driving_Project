export default function LogViewer({ logs }) {
  return (
    <div className="card">
      <h3>Behavior Logs</h3>
      <pre>{JSON.stringify(logs, null, 2)}</pre>
    </div>
  );
}
