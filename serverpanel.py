"""
Copyright  2021 All rights reserved by Edussm Inc.
"""
import os

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

class operations(tools):

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
            



class views(operations):
   def domain_panel(self):
      self.execute("clear")
      print("""
      !!--Domain Panel --!!

      1.Add Domain
      2.Create Subdomain
      3.View Domains

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
         


   def window_main(self):
      self.execute("clear")
      print("""
      Welcome  to  server panel edussm

      1. Domain panel.
      """)
      self.get_command()

      if COMMAND == "1":
         self.domain_panel()
      

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
   panel.run()