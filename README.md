# mbed_exam2

更改accelorometer_handler.cpp float ReadAccelerometer(tflite::ErrorReporter* error_reporter, float* input,int length, bool reset_buffer)會return float type
算出加速器的數值平均return

在main裡會更據回傳的float判斷大於0或小於0，plot到圖上
client.cpp負責RPC指令及收資料
