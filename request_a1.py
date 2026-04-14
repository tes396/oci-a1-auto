import oci
import os
import datetime

config = oci.config.from_file()
compute = oci.core.ComputeClient(config)
compartment_id = os.environ['COMPARTMENT_ID']

print(f"実行時刻: {datetime.datetime.now()}")

try:
    response = compute.launch_instance(
        oci.core.models.LaunchInstanceDetails(
            compartment_id=compartment_id,
            availability_domain="DcLl:AP-SINGAPORE-1-AD-1",
            shape="VM.Standard.A1.Flex",
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=4,
                memory_in_gbs=24
            ),
            display_name="a1-auto-instance",
            subnet_id="ocid1.subnet.oc1.ap-singapore-1.aaaaaaaahyfr367wypubaq37nb4s3w2axartkor4jporn6ljkpchqbs44xla",
            create_vnic_details=oci.core.models.CreateVnicDetails(
                assign_public_ip=True,
                subnet_id="ocid1.subnet.oc1.ap-singapore-1.aaaaaaaahyfr367wypubaq37nb4s3w2axartkor4jporn6ljkpchqbs44xla"
            ),
            metadata={
                "ssh_authorized_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDhN/F+Gvcin+gNkMcjk768Ppnqf6TJqQWKO9Aw3XcdOS4j6Aqwbnp1ZnS9J3PqsT4f9Ighc7bMyTUzxXhc+3rci1NhqwYThRMZD++VPV35JtLX5bZ5yqLNTMOZ61aV5O1NRiAVFxG0c6LDOQPzN4s8rEsC0bhcFM9HlLIfAnT4HgqcYRsxwJWnXm3ltqIQjLpgIiu/hftyEjRnE+Ywc7mxYlcrnbwqLMNMa7ZhCZf+x2AwJ5UTN1l9vw3rPduYAVMGApoSga5L3fGGKRGmDmbIT5bUFB4HT9ES0yfXnWWEt+CiTTVBe1QpagHgax9be5Drl5j8VFVJ5sSmC6QcvNHB akhr_nk014@af921f4d3bbf"
            }
        )
    )
    print("✅ インスタンス作成成功！")
    print(response.data)
except oci.exceptions.ServiceError as e:
    if "Out of capacity" in str(e):
        print("⚠️ 容量不足 - 次回再試行します")
    elif e.status == 429:
        print("⚠️ リクエスト過多 - 次回再試行します")
    else:
        print(f"エラー: {e}")
