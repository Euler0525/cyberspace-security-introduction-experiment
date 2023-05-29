#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char input[] = "";

void inject()  // 栈溢出的目的是让inject程序运行
{
    printf("*****inject success*****\n");
}

void func_call()  // 正常调用的函数
{
    char param[16];
    strcpy(param, input);
}

int main(int argc, char** argv)
{
    func_call();
    printf("main exit...\n");
    return 0;
}
