using System;
using RabbitMQ.Client;

// https://www.rabbitmq.com/dotnet-api-guide.html
// https://www.rabbitmq.com/tutorials/tutorial-six-dotnet.html

namespace client
{
    class Program
    {
        static void Main(string[] args)
        {
            var factory = new ConnectionFactory()
            {
                UserName = "mirero",
                Password = "system",
                VirtualHost = "/",
                HostName = "192.168.100.76"
            };


            using var conn = factory.CreateConnection();
            using var rpcClient = new RpcClient(conn);

            Console.WriteLine("Hello ->");
            var response = rpcClient.Call("Hello", 1000);

            Console.WriteLine("<- {0}", response);
        }
    }
}
