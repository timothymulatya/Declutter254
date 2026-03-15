import { approveRequest, rejectRequest, markAsGiven } from "../api/api"

function RequestActions({ request, refreshRequests }) {

  function handleApprove() {

    approveRequest(request.id)
      .then(() => refreshRequests())

  }

  function handleReject() {

    rejectRequest(request.id)
      .then(() => refreshRequests())

  }

  if (request.status !== "pending") {
    return null
  }

  return (

    <div style={{ marginTop: "10px" }}>

      <button
        onClick={handleApprove}
        style={{ marginRight: "10px", background: "green", color: "white" }}
      >
        Approve
      </button>

      <button
        onClick={handleReject}
        style={{ background: "red", color: "white" }}
      >
        Reject
      </button>

    </div>

  )

}

export default RequestActions 