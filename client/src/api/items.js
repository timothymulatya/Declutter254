export function approveRequest(requestId){

  return fetch(`/requests/${requestId}/approve`,{
    method:"PATCH"
  })
  .then(res => res.json())

}


export function rejectRequest(requestId){

  return fetch(`/requests/${requestId}/reject`,{
    method:"PATCH"
  })
  .then(res => res.json())

} 