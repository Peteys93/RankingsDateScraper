using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using HtmlAgilityPack;
using OpenQA.Selenium;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Test");

            HtmlWeb web = new HtmlWeb();
            HtmlDocument document = web.Load("https://rankings.the-elite.net/goldeneye/stage/dam");
           
            var links = document.DocumentNode.SelectNodes("//a");
            var links2 =document.DocumentNode.SelectNodes("//*[@id='diff-0']/table/tr");


            foreach (HtmlNode item in links)
            {
                Console.WriteLine(item.InnerHtml);
            }

            Console.ReadKey();
            }
        }
    }
