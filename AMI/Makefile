
# EC2_HOME        = ./ec2-api-tools-1.4.4.2 this is old one
EC2_HOME        = ./ec2-api-tools-1.7.5.1
AWS_ACCESS_KEY = 
AWS_SECRET_KEY = 
EC2_ZONE        = us-east-1b
EC2_URL         = https://ec2.us-east-1.amazonaws.com

# The seed AMI is Basic Amazon Linux 64-bit 2011.09
#AMI_ID          = ami-28670341
#AMI_ID          = ami-7341831a
#  ami-1ecae776 is for HVM  amzn-ami-hvm-2015.03.0.x86_64-gp2 - ami-1ecae776
#  amzn-ami-hvm-2014.03.2.x86_64-ebs - ami-76817c1e
#
#AMI_ID          = ami-1ecae776  (this one is old one)
AMI_ID = ami-76817c1e

#INSTANCE_TYPE = m1.xlarge
# for HVM type, use m3.xlarge
INSTANCE_TYPE = i2.xlarge
INSTANCE_HOST = `grep INSTANCE instance-describe.out | grep 'sandip2-ami' | cut -f 4`
INSTANCE_ID   = `grep INSTANCE instance-describe.out | grep 'sandip2-ami' | cut -f 2`

# old amazon ami id
OLD_INSTANCE_ID 	    = i-e67a0883

SSH_KEY = sandip2-ami
SSH_CMD = ssh -i ~/.ssh/$(SSH_KEY).pem ec2-user@$(INSTANCE_HOST)

VERSION = 4.6.0
IMAGE_NAME = couchbase_server_enterprise_x86_64-${VERSION}
#IMAGE_DESC = pre-installed Couchbase Server ${VERSION}, Community Edition, 64bit
#IMAGE_NAME = couchbase_server_community_edition__x86_64_${VERSION}
IMAGE_DESC = pre-installed Couchbase Server ${VERSION}, Enterprise Edition, 64bit

#PKG_BASE = http://builder.hq.couchbase.com/get
#PKG_BASE = http://packages.couchbase.com/releases/${VERSION}
PKG_BASE = http://packages.couchbase.com/releases/${VERSION}
#PKG_NAME = couchbase-server-community-${VERSION}-centos6.x86_64.rpm
PKG_NAME = couchbase-server-enterprise-${VERSION}-centos6.x86_64.rpm
#PKG_NAME = couchbase-server-enterprise_centos6_x86_64_${VERSION}-rel.rpm
# full url look like this
# http://packages.couchbase.com/releases/3.1.1/couchbase-server-enterprise-3.1.1-centos6.x86_64.rpm
#https://s3-us-west-2.amazonaws.com/cb-binaries/4.5.0/couchbase-server-enterprise-4.5.0-centos6.x86_64.rpm
PKG_KIND = couchbase
CLI_NAME = couchbase-cli

SECURITY_GROUP = couchbase-2016

VOLUME_ID = `grep VOLUME volume-describe.out | cut -f 2`
VOLUME_GB = 80

SNAPSHOT_ID = `grep SNAPSHOT snapshot-describe.out | cut -f 2`

step0: \
    instance-launch

step1: \
    instance-describe \
    instance-clean \
    instance-update
 
step2: \
    instance-prep

step3: \
    instance-prep-pkg 

step4: \
    volume-create \
    volume-attach \
    volume-mkfs \
    snapshot-create \
    volume-mount

step5: \
    instance-cleanse \
    instance-image-create

describe-image:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    $(EC2_HOME)/bin/ec2-describe-images -o amazon --filter "image-type=kernel"

generate-key:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    $(EC2_HOME)/bin/ec2-create-keypair ${SSH_KEY} > ${SSH_KEY}
	cp ${SSH_KEY} ~/.ssh/

instance-launch:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-run-instances $(AMI_ID) \
      --block-device-mapping /dev/sdb=ephemeral0 \
      --block-device-mapping /dev/sdc=ephemeral1 \
      --block-device-mapping /dev/sdd=ephemeral2 \
      --block-device-mapping /dev/sde=ephemeral3 \
      --availability-zone $(EC2_ZONE) \
      --instance-type $(INSTANCE_TYPE) \
      --instance-initiated-shutdown-behavior stop \
      --group $(SECURITY_GROUP) \
      --key $(SSH_KEY) > instance-describe.out
	sleep 60
	$(MAKE) instance-describe
	cat instance-describe.out

instance-describe:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-describe-instances $(INSTANCE_ID) > instance-describe.out
	cat instance-describe.out

instance-clean:
	$(SSH_CMD) yum clean all

instance-update:
	 $(SSH_CMD) -t sudo yum update

instance-prep:
	scp -i ~/.ssh/$(SSH_KEY).pem prep \
      ec2-user@$(INSTANCE_HOST):/home/ec2-user/prep
	$(SSH_CMD) -t sudo /home/ec2-user/prep

instance-prep-pkg:
	$(SSH_CMD) wget https://s3.amazonaws.com/couchbasescript/Couchbaseinit.sh | \
	$(SSH_CMD) curl -O https://bootstrap.pypa.io/get-pip.py | \
        $(SSH_CMD) wget -O $(PKG_NAME) $(PKG_BASE)/$(PKG_NAME)
	sed -e s,@@PKG_NAME@@,$(PKG_NAME),g README.txt.tmpl | \
      sed -e s,@@PKG_KIND@@,$(PKG_KIND),g | \
      sed -e s,@@CLI_NAME@@,$(CLI_NAME),g > README.txt.out
	sed -e s,@@PKG_NAME@@,$(PKG_NAME),g config-pkg.tmpl | \
      sed -e s,@@PKG_KIND@@,$(PKG_KIND),g | \
      sed -e s,@@CLI_NAME@@,$(CLI_NAME),g > config-pkg.out
	chmod a+x config-pkg.out
	scp -i ~/.ssh/$(SSH_KEY).pem README.txt.out \
      ec2-user@$(INSTANCE_HOST):/home/ec2-user/README.txt
	scp -i ~/.ssh/$(SSH_KEY).pem config-pkg.out \
      ec2-user@$(INSTANCE_HOST):/home/ec2-user/config-pkg
	$(SSH_CMD) -t sudo mkdir -p /var/lib/cloud/data/scripts
	$(SSH_CMD) -t sudo cp /home/ec2-user/config-pkg /var/lib/cloud/data/scripts/config-pkg
	$(SSH_CMD) -t sudo chown root:root /var/lib/cloud/data/scripts/config-pkg | \
	$(SSH_CMD) -t sudo cp /home/ec2-user/Couchbaseinit.sh /var/lib/cloud/data/scripts/Couchbaseinit.sh | \
        $(SSH_CMD) -t sudo chown root:root /home/ec2-user/Couchbaseinit.sh | \
        $(SSH_CMD) -t sudo chown root:root /home/ec2-user/get-pip.py | \
	$(SSH_CMD) -t sudo chmod a+x /home/ec2-user/Couchbaseinit.sh | \
	$(SSH_CMD) -t sudo python27 /home/ec2-user/get-pip.py | \
        $(SSH_CMD) -t sudo sleep 60 | \
	$(SSH_CMD) -t sudo /usr/local/bin/pip install awscli | \
        $(SSH_CMD) -t sudo ln -s /usr/bin/aws /usr/local/bin/aws

instance-cleanse:
	$(SSH_CMD) -t sudo rm -f \
      /home/ec2-user/.bash_history \
      /home/ec2-user/.ssh/authorized_keys \
      /home/ec2-user/*.tmp \
      /home/ec2-user/*~ \
      /root/.bash_history \
      /root/.ssh/authorized_keys \
      /root/*.tmp \
      /root/*~

list-amis:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
    $(EC2_HOME)/bin/ec2-stop-instances ${INSTANCE_ID}

instance-image-create:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-create-image \
      --name "$(IMAGE_NAME)" \
      --description "$(IMAGE_DESC)" \
      $(INSTANCE_ID)

instance-image-recreate:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-create-image $(OLD_INSTANCE_ID) \
      --name "$(IMAGE_NAME)" \
      --description "$(IMAGE_DESC)"

instance-stop:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
    $(EC2_HOME)/bin/ec2-stop-instances $(INSTANCE_ID)

volume-create:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-create-volume \
      --availability-zone $(EC2_ZONE) \
      --size $(VOLUME_GB) > volume-describe.out \
	sleep 60

volume-create-from-snapshot:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-create-volume \
      --availability-zone $(EC2_ZONE) \
      --size $(VOLUME_GB) \
      --snapshot $(SNAPSHOT_ID) > volume-describe.out

volume-describe:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-describe-volumes $(VOLUME_ID)

volume-attach:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-attach-volume $(VOLUME_ID) \
      --instance $(INSTANCE_ID) \
      --device /dev/sdh
	sleep 60

volume-mkfs:
	$(SSH_CMD) -t sudo mkfs.ext3 /dev/sdh

volume-mount:
	$(SSH_CMD) -t sudo mkdir -p /mnt
	$(SSH_CMD) -t sudo mkdir -m 000 /mnt/ebs
	$(SSH_CMD) -t "echo /dev/sdh /mnt/ebs ext3 noatime 0 0 | sudo tee -a /etc/fstab"
	$(SSH_CMD) -t sudo mount -a

snapshot-create:
	EC2_HOME=$(EC2_HOME) \
    AWS_ACCESS_KEY=$(AWS_ACCESS_KEY) \
    AWS_SECRET_KEY=$(AWS_SECRET_KEY) \
    EC2_URL=$(EC2_URL) \
      $(EC2_HOME)/bin/ec2-create-snapshot $(VOLUME_ID) \
      --description empty-ext3-$(VOLUME_GB)gb > snapshot-describe.out

clean:
	rm -f *.out
