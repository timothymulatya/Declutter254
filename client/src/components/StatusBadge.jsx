function StatusBadge({ status }) {

  let color = "gray"

  if (status === "pending") color = "orange"
  if (status === "approved") color = "green"
  if (status === "rejected") color = "red"
  if (status === "given") color = "blue"

  const style = {
    padding: "5px 10px",
    borderRadius: "5px",
    backgroundColor: color,
    color: "white",
    fontSize: "12px"
  }

  return <span style={style}>{status}</span>

}

export default StatusBadge 