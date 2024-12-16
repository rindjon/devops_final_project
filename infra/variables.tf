variable "ami" {
  default = "ami-0453ec754f44f9a4a"
}

variable "instance_type" {
  default = "t2.medium"
}

variable "ssh_key_name" {
  type    = string
  default = "vockey"
}

variable "sg_map" {
  default = {
        "GitHub_Runner" = {
            extra_ports = [ 443 ]
        },
        "K8S_Cluster" = {
          extra_ports = [ 80 ]
        }
    }
}

variable "ec2_map" {
  default = {
        "GitHub_Runner" = {}
        "K8S_Cluster" = {}
    }
}


#   user_data = <<-EOF
#     #!/bin/bash
#     sudo yum update -y
#     sudo yum install -y libicu
#     mkdir actions-runner && cd actions-runner
#     curl -o actions-runner-linux-x64-2.321.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.321.0/actions-runner-linux-x64-2.321.0.tar.gz
#     tar xzf ./actions-runner-linux-x64-2.321.0.tar.gz
#     ./config.sh --url https://github.com/d4v5he/gh_arc --token BH74YWKX2QMP53C3273Y7OLHLPTNM --unattended --replace
#     sudo ./svc.sh install
#     sudo ./svc.sh start
#   EOF
