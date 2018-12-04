# Conformance rules

Rule Id   | Description
----- ----|------------
TAC1      | The Access Token shall be formatted as defined in Section 2 of [URISigning](https://tools.ietf.org/html/draft-ietf-cdni-uri-signing-16) (i.e. a JSON Web Token)
TAC2      | The CDNI Signed Token Transport (cdnistt) claim value of any Access Token shall be “2” (i.e. DASH-IF transport)
TAC3      | The DASH-IF-IETF-Token HTTP header shall only be present in HTTP 2xx successful message.
TAC4      | If present, The DASH-IF-IETF-Token HTTP header shall contain an encoded Access Token as defined in [URISigning](https://tools.ietf.org/html/draft-ietf-cdni-uri-signing-16).
TAC5      | If present, the dash-if-ietf-token query string shall contain an encoded Access Token as defined in [URISigning] and formatted according to rules TAC1 and TAC2.
