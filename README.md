# TAC Conformance Server

HTTP server conformance for TAC

## REST API

/mpds

Return a list of MPDs that can be used with the TAC server

/mpds/:id?mode=proxy|validation|simulation

Returns an MPD configured for the requested mode:

  - 'proxy', the requests will be proxied to the original server
  - 'validation', the incoming HTTP requests and the HTTP response from
  original server will be validated against the TAC conformance
  - 'simulation', the MPD and HTTP responses from the original server
  are augmented to simulate TAC. Note that this does not implement a real
  token-base access control but merely simulates the TAC signalling
