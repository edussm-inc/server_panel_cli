"""
Copyright  2021 All rights reserved by Edussm Inc.
"""
import os
from pprint import pprint
import sys
from os import path

ETC = "/etc/"
APACHE_SERVER = "/etc/httpd"
SITES_AVAILABLE = APACHE_SERVER+"/sites-available/"
SITES_ENABLED = APACHE_SERVER+"/sites-enabled/"
WEB_ROOT = "/var/www/"
COMMAND = ""

# tool  class
class tools:

   def execute(self, text):
      os.system(text)

   def get_command(self):
      global  COMMAND
      c = input(" serverpanel> ")
      COMMAND = c
      return c

   def write_file(self, filename, content):
      f = open(filename, "w")
      f.write(content)
      f.close()
      return True

   def remove_file(self, filename):
      os.remove(filename);
      return 1
      

class operations(tools):

   def Setup_apache(self):
       print("Apache server setup started....")
       self.execute(f"sudo yum install update")
       print("Installing httpd......")
       self.execute(f"sudo yum install httpd")
       print("Adding service to firewall ....")
       self.execute(f"sudo firewall-cmd --permanent --add-service=https")
       print("Reloading firwall")
       self.execute(f"sudo firewall-cmd --reload")
       print("Starting httpd....")
       self.execute(f"sudo systemctl start httpd");
       print("Setting success.... now run the script again to get panel and go to your ip address to access web")

   def create_domain_config(self,  domain_name):
      print("PLease wait adding domain..")
      self.execute(f"sudo mkdir -p {WEB_ROOT+domain_name}/public_html")
      print("working...")
      self.execute(f"sudo mkdir -p {WEB_ROOT+domain_name}/log")
      print("working...")
      self.execute(f"sudo chown -R $USER:$USER {WEB_ROOT+domain_name}/public_html")
      print("working...")
      genrate_index_file = WEB_ROOT+domain_name+"/public_html/index.html"
      self.write_file(genrate_index_file, "<h1>Successfully working</h1>")
      print("working...")
      self.execute(f"sudo chown -R $USER:$USER {WEB_ROOT+domain_name}/public_html")
      print("working...")
      genrate_domain_config = SITES_AVAILABLE+domain_name+".conf"
      domain_config_content = f"""
      <VirtualHost *:80>
         ServerName {domain_name}
         ServerAlias www.{domain_name}
         DocumentRoot /var/www/{domain_name}/public_html
         ErrorLog /var/www/{domain_name}/log/error.log
         CustomLog /var/www/{domain_name}/log/requests.log combined
      </VirtualHost>
      """
      self.write_file(genrate_domain_config, domain_config_content)
      print("working...")
      self.execute(f"sudo ln -s {SITES_AVAILABLE+domain_name}.conf {SITES_ENABLED+domain_name}.conf")
      print("working...")
      self.execute(f"sudo ls -dZ {WEB_ROOT+domain_name}/log/")
      print("working...")
      self.execute(f"sudo semanage fcontext -a -t httpd_log_t '{WEB_ROOT+domain_name}/log(/.*)?'")
      print("working...")
      self.execute(f"sudo restorecon -R -v {WEB_ROOT+domain_name}/log")
      print("working...")
      self.execute(f"sudo ls -dZ {WEB_ROOT+domain_name}/log/")
      print("working...")
      self.execute(f"sudo systemctl restart httpd")
      print("working...")
      self.execute(f"ls -lZ {WEB_ROOT+domain_name}/log")
      print("Successfully added domain")
   
   def add_domain(self):
      self.execute("clear")
      domain_name = input("Enter domain name: ")
      self.create_domain_config(domain_name)
      

   def view_domains(self):
      self.execute("clear")
      domains_config = os.listdir(SITES_AVAILABLE)
      print(" Domains:")
      i = 1
      for domain in domains_config:
         split_res = domain.split(".")
         if split_res[len(split_res) - 1] == "conf":
            domain = domain.replace(".conf", "")
            print(" "+str(i)+". "+domain)
            i += 1

   def get_domains(self):
      domains_config = os.listdir(SITES_AVAILABLE)
      domains = []
      for domain in domains_config:
         split_res = domain.split(".")
         if split_res[len(split_res) - 1] == "conf":
            domain = domain.replace(".conf", "")
            domains.append(domain)

      return domains
   
   def set_proxy_server(self, proxypass, selected_domain):
      print("PLease wait Configuring domain..")
      domain_config = SITES_AVAILABLE+selected_domain+".conf"
      domain_config_content = f"""
      <VirtualHost *:80>
         ServerName {selected_domain}
         ServerAlias www.{selected_domain}
         DocumentRoot {WEB_ROOT+selected_domain}/{selected_domain}/public_html
         ErrorLog {WEB_ROOT+selected_domain}/{selected_domain}/log/error.log
         CustomLog {WEB_ROOT+selected_domain}/{selected_domain}/log/requests.log combined
         ProxyPreserveHost On
         ProxyPass / {proxypass}
         ProxyPassReverse / {proxypass}
      </VirtualHost>
      """
      self.write_file(domain_config, domain_config_content)
      print("Successfully added Proxy on: ", selected_domain)
      print("Proxy pass: ", proxypass)

   def create_subdomain(self, subdomain_name, selected_domain):
      subdomain_name = subdomain_name+"."+selected_domain
      print("PLease wait adding subdomain..")
      self.execute(f"sudo mkdir -p {WEB_ROOT+selected_domain}/{subdomain_name}/public_html")
      print("working...")
      self.execute(f"sudo mkdir -p {WEB_ROOT+selected_domain}/{subdomain_name}/log")
      print("working...")
      self.execute(f"sudo chown -R $USER:$USER {WEB_ROOT+selected_domain}/{subdomain_name}/public_html")
      print("working...")
      genrate_index_file = WEB_ROOT+selected_domain+"/"+subdomain_name+"/public_html/index.html"
      self.write_file(genrate_index_file, "<h1>Successfully working</h1>")
      print("working...")
      self.execute(f"sudo chown -R $USER:$USER {WEB_ROOT+selected_domain}/{subdomain_name}/public_html")
      print("working...")
      genrate_domain_config = SITES_AVAILABLE+subdomain_name+".conf"
      domain_config_content = f"""
      <VirtualHost *:80>
         ServerName {subdomain_name}
         ServerAlias www.{subdomain_name}
         DocumentRoot {WEB_ROOT+selected_domain}/{subdomain_name}/public_html
         ErrorLog {WEB_ROOT+selected_domain}/{subdomain_name}/log/error.log
         CustomLog {WEB_ROOT+selected_domain}/{subdomain_name}/log/requests.log combined
      </VirtualHost>
      """
      self.write_file(genrate_domain_config, domain_config_content)
      print("working...")
      self.execute(f"sudo ln -s {SITES_AVAILABLE+subdomain_name}.conf {SITES_ENABLED+subdomain_name}.conf")
      print("working...")
      self.execute(f"sudo ls -dZ {WEB_ROOT+selected_domain}/{subdomain_name}/log/")
      print("working...")
      self.execute(f"sudo semanage fcontext -a -t httpd_log_t '{WEB_ROOT+selected_domain}/{subdomain_name}/log(/.*)?'")
      print("working...")
      self.execute(f"sudo restorecon -R -v {WEB_ROOT+selected_domain}/{subdomain_name}/log")
      print("working...")
      self.execute(f"sudo ls -dZ {WEB_ROOT+selected_domain}/{subdomain_name}/log/")
      print("working...")
      self.execute(f"sudo systemctl restart httpd")
      print("working...")
      self.execute(f"ls -lZ {WEB_ROOT+selected_domain}/{subdomain_name}/log")
      print("Successfully added subdomain")

   def remove_domain(self):
      self.execute("clear")
      print(" Please choose a domain: ")
      domains = self.get_domains()
      i = 1
      for domain in domains:
         print(" "+str(i)+". "+domain)
         i += 1
      get_domain = input(" Domain No>>> ")
      get_domain = int(get_domain) - 1
      selected_domain = domains[get_domain]
      confirm = input("Are you sure to delete this domain?(y/n) ")
      if confirm == "y":
         print("Removing domain...")
         self.execute(f"sudo rm -f {SITES_AVAILABLE+selected_domain}.conf")
         self.execute(f"sudo rm -f {SITES_ENABLED+selected_domain}.conf")
         print(f" `{selected_domain}` domain removed successfully !!")
      else:
         self.remove_domain()
            



class views(operations):
   def domain_panel(self):
      self.execute("clear")
      print("""
      !!--Domain Panel --!!

      1.Add Domain
      2.Create Subdomain
      3.View Domains
      4.remove domain

      0 FOR BACK
      00 FOR GO HOME
      """)
      self.get_command()

      if COMMAND  == "0":
         self.window_main()

      elif COMMAND  == "00":
         self.window_main()
      elif COMMAND  == "1":
         self.add_domain()
      elif COMMAND  == "2":
         self.subdomain_creating()
      elif COMMAND  == "3":
         self.view_domains()
      elif COMMAND == "4":
         self.remove_domain()

   def subdomain_creating(self):
      self.execute("clear")
      print(" Please choose a domain: ")
      domains = self.get_domains()
      i = 1
      for domain in domains:
         print(" "+str(i)+". "+domain)
         i += 1
      get_domain = input(" Domain No>>> ")
      get_domain = int(get_domain) - 1
      selected_domain = domains[get_domain]
      subdomain_name = input(" Subdomain name>> ")
      self.create_subdomain(subdomain_name, selected_domain)
   
   def setting_proxy_server(self):
      self.execute("clear")
      print(" Please choose a domain where you wnat to set proxy: ")
      domains = self.get_domains()
      i = 1
      for domain in domains:
         print(" "+str(i)+". "+domain)
         i += 1
      get_domain = input(" Domain No>>> ")
      get_domain = int(get_domain) - 1
      selected_domain = domains[get_domain]
      ProxyPass = input(" Proxy Pass & Reverse (IP & PORT HERE - Example: http://127.0.0.1:8080/)>> ")
      self.set_proxy_server(ProxyPass, selected_domain)
   
   def Manage_virtual_host(self):
      self.execute("clear")
      print("""
      !!--Manage Virtual Host --!!

      1.Set Proxy Server.

      0 FOR BACK
      00 FOR GO HOME
      """)
      self.get_command()

      if COMMAND  == "0":
         self.window_main()

      elif COMMAND  == "00":
         self.window_main()
      elif COMMAND  == "1":
         self.setting_proxy_server()
         
      


   def window_main(self):
      self.execute("clear")
      print("""
      Welcome  to  server panel edussm

      1. Domain panel.
      2. Manage Virtual Host.
      """)
      self.get_command()

      if COMMAND == "1":
         self.domain_panel()
      elif COMMAND == "2":
         self.Manage_virtual_host()
         pass
      

class serverpanel(views):

   def write_domain_config_file(self):
      genrate_path = APACHE_SERVER+"/test.txt"
      self.write_file(genrate_path, "Hello my name is sami")
      print("File successfully created")

   def run(self):
      self.window_main()
      # self.write_domain_config_file();


if __name__ == '__main__':
   panel = serverpanel()
   arg_len = len(sys.argv)
   argv = sys.argv
   if arg_len > 1:
     i = 1
     for item in argv:
      if item == "setup:apache":
        panel.Setup_apache()
   else:
    panel.run()
