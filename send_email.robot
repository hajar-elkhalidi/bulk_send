*** Settings ***
Library     RPA.Email.ImapSmtp    smtp_server=smtp.gmail.com    smtp_port=587
Library     Collections
Library     OperatingSystem
Library     RPA.Browser.Selenium

Resource    resources/email.resource
Resource    resources/recipients_emails.resource

*** Variables ***
${email}      NONE
${app_pass}   NONE

*** Tasks ***
Send Email
    [Documentation]    Send email with CV attachment to multiple recipients.
    Authorize    ${email}    ${app_pass}
    FOR    ${RECIPIENT}    IN    @{RECIPIENTS}
        Send Email To Recipient    ${RECIPIENT}
    END

*** Keywords ***
Send Email To Recipient
    [Arguments]    ${RECIPIENT}
    Log    Sending email to ${RECIPIENT}
    Send Message    sender=${email}    recipients=${RECIPIENT}    subject=${EMAIL_SUBJECT}    
    ...    body=${EMAIL_BODY}    attachments=${ATTACHMENT_PATH}