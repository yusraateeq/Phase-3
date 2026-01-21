Chat


POST
/api/chat
Chat


Parameters
Cancel
Reset
No parameters

Request body

application/json
Edit Value
Schema
{
  "message": "Hello",
  "conversation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
Execute
Clear
Responses
Curl

curl -X 'POST' \
  'https://yusraateeq-fullstack-phase-3.hf.space/api/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "Hello",
  "conversation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}'
Request URL
https://yusraateeq-fullstack-phase-3.hf.space/api/chat
Server response
Code	Details
401
Undocumented
Error: response status is 401

Response body
Download
{
  "detail": "Not authenticated"
}
Response headers
 access-control-allow-credentials: true 
 access-control-allow-origin: https://yusraateeq-fullstack-phase-3.hf.space 
 content-length: 30 
 content-type: application/json 
 date: Wed,21 Jan 2026 09:30:19 GMT 
 link: <https://huggingface.co/spaces/yusraateeq/Fullstack-Phase-3>;rel="canonical" 
 server: uvicorn 
 vary: origin,access-control-request-method,access-control-request-headers 
 www-authenticate: Bearer 
 x-process-time: 0.0008955001831054688 
 x-proxied-host: http://10.108.45.116 
 x-proxied-path: /api/chat 
 x-proxied-replica: io6qcuoe-dpbwb 
 x-request-id: NdO_A6 
Responses
Code	Description	Links
200	
Successful Response

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "message": "string",
  "conversation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
No links
422	
Validation Error

Media type

application/json
Example Value
Schema
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}