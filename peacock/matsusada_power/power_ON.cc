#include <iostream> //標準入出力
#include <bits/stdc++.h>
#include <sys/socket.h> //アドレスドメイン
#include <sys/types.h> //ソケットタイプ
#include <arpa/inet.h> //バイトオーダの変換に利用
#include <unistd.h> //close()に利用
#include <string> //string型
#include <string.h>

int main(){
  //ソケットの生成
  int sockfd = socket(AF_INET, SOCK_STREAM, 0); //アドレスドメイン, ソケットタイプ, プロトコル
  if(sockfd < 0){ //エラー処理

    std::cout << "Error socket:" << std::strerror(errno); //標準出力
    exit(1); //異常終了
  }

  //アドレスの生成
  struct sockaddr_in addr; //接続先の情報用の構造体(ipv4)
  memset(&addr, 0, sizeof(struct sockaddr_in)); //memsetで初期化
  addr.sin_family = AF_INET; //アドレスファミリ(ipv4)
  addr.sin_port = htons(10001); //ポート番号,htons()関数は16bitホストバイトオーダーをネットワークバイトオーダーに変換
  addr.sin_addr.s_addr = inet_addr("192.168.1.248"); //IPアドレス,inet_addr()関数はアドレスの翻訳

  //ソケット接続要求
  connect(sockfd, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)); //ソケット, アドレスポインタ, アドレスサイズ

  //データ送信
  //char s_str[] = "\x23\x31\x20\x52\x45\x4e\x20\x0d";//#1 REN
  char output[] = "#1 SW1 \r";

  int output_num = strlen(output);

  send(sockfd, output , output_num, 0); //送信
  std::cout << output << std::endl;
    
  //データ受信
  //char r_str[] = {}; //受信データ格納用
  //recv(sockfd, r_str, strlen(r_str), 0); //受信
  //std::cout << r_str << std::endl; //標準出力
  //ソケットクローズ
  close(sockfd);

  return 0;
}
