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
          extra_ports = [ 30080 ]
        }
    }
}

variable "ec2_map" {
  default = {
        "GitHub_Runner" = {
            user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y libicu
              mkdir actions-runner && cd actions-runner
              curl -o actions-runner-linux-x64-2.321.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.321.0/actions-runner-linux-x64-2.321.0.tar.gz
              tar xzf ./actions-runner-linux-x64-2.321.0.tar.gz
              ./config.sh --url https://github.com/rindjon/devops_final_project --token AGT5EORQUJSUSE4L6HCRZTDHNZ25M --unattended
              sudo ./svc.sh install
              sudo ./svc.sh start
            EOF
        }
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
#     ./config.sh --url https://github.com/rindjon/devops_final_project --token AGT5EOQQXJ6IT75U723J53THNPL6K --unattended --replace
#     sudo ./svc.sh install
#     sudo ./svc.sh start
#   EOF
