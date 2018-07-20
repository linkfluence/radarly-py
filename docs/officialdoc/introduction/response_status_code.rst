Response status code
~~~~~~~~~~~~~~~~~~~~

Success
    Successes differ from errors in that their body may not be a
    simple response object with a code and a message. The headers
    however are consistent across all calls:

        * GET, PUT, DELETE returns 200 OK on success,
        * POST returns 201 on success,

Error
    Error responses are simply returning standard HTTP error
    codes along with some additional information. The error
    code is sent back as a status header. The body includes an
    object describing both the code and message (for debugging
    and/or display purposes).
