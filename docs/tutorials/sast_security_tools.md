### SAST Tools: how to use them

##### installation
The tools are in requirements.txt, so re-run pip install:
```bash
$ pip install -r requirements.txt
```


##### pip-audit
```bash
# looks for vulnerabilities in requirements.txt, no changes are made to the file
$ pip-audit -r requirements.txt --strict
```

##### bandit
```bash
# find vulnerabilities and print report to the terminal
$ bandit -r .

# generate a json report
$ bandit -r -f json -o bandit.json .

# generate a HTML report file listing "medium" and "high" severity vulnerabilities.
$ bandit -r --severity-level=medium -f html -o bandit_report.html .

# generate a HTML report but exclude a directory named "venv"
$ bandit -r -f html -x ./venv -o bandit_report.html .
```

##### secure.py

Security headers are set on every response. The *Content Security Policy (CSP)* is configured in: app/__init__.py:create_app

To configure the CSP settings, modify the `add_security_headers()` function:

```python
def _add_security_headers(response):
    """ add security headers, allow external assets for Bootstrap, jQuery, Font Awesome"""
    secure_headers.set_headers(response)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com https://cdnjs.cloudflare.com https://code.jquery.com https://kit.fontawesome.com;"
        "script-src 'self' 'unsafe-inline'  https://code.jquery.com https://cdnjs.cloudflare.com https://kit.fontawesome.com; "
        "img-src 'self' https://placehold.co; "
        "font-src 'self' https://fonts.gstatic.com https://ka-f.fontawesome.com; " 
        "connect-src 'self' https://ka-f.fontawesome.com; "
    )
    return response
```

