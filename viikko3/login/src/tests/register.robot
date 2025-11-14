*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Go To Register Page
    Set Username  newuser
    Set Password  CorrectPassw1
    Set Password Confirmation  CorrectPassw1
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  aa
    Set Password  CorrectPassw1
    Click Button  Register
Register Should Fail With Message    Username too short

Register With Valid Username And Too Short Password
    Set Username  correctuser
    Set Password  u123
    Set Password Confirmation  u123
    Click Button  Register
Register Should Fail With Message    Password too short

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Go To Register Page
    Set Username  correctuser
    Set Password  letters
    Set Password Confirmation  letters
    Click Button  Register
    Register Should Fail With Message    Password must only contain letters and numbers

Register With Nonmatching Password And Password Confirmation
    Go To Register Page
    Set Username  newuser
    Set Password  CorrectPassw00
    Set Password Confirmation  DifferentPassw1
    Click Button  Register
    Register Should Fail With Message    Passwords do not match

Register With Username That Is Already In Use
    Create User  olduser  Password123
    Go To Register Page
    Set Username  olduser
    Set Password  Password123
    Set Password Confirmation  Password123
    Click Button  Register
    Register Should Fail With Message    Username already exists

*** Keywords ***


Go To Register Page
    Go To  ${REGISTER_URL}

Register Page Should Be Open
    Title Should Be    Register

Set Username
    [Arguments]    ${username}
    Input Text  username    ${username}

Set Password 
    [Arguments]    ${password}
    Input Password  password    ${password}

Set Password Confirmation
    [Arguments]    ${password}
    Input Password    password_confirmation    ${password}

Register Should Succeed
    Page Should Contain    Welcome to Ohtu Application!

Register Should Fail With Message
    [Arguments]    ${message}
    Register Page Should Be Open
    Page Should Contain    ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User    newuser2    CorrectPassw1
    Go To Register Page
