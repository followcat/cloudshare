from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient


def send_sms(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION, business_id, phone_number,
             sign_name, template_code, template_param=None):
    if isinstance(sign_name, unicode):
        sign_name = sign_name.encode('utf-8')
    acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
    smsRequest = SendSmsRequest.SendSmsRequest()
    smsRequest.set_TemplateCode(template_code)
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    smsRequest.set_OutId(business_id)
    smsRequest.set_SignName(sign_name);
    smsRequest.set_PhoneNumbers(phone_number)
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse
