import oci
import os
import datetime

config = oci.config.from_file()
compute = oci.core.ComputeClient(config)
compartment_id = os.environ['COMPARTMENT_ID']
subnet_id = os.environ['SUBNET_ID']
ssh_public_key = os.environ['SSH_PUBLIC_KEY']
image_id = os.environ['IMAGE_ID']  # ← 追加

print(f"実行時刻: {datetime.datetime.now()}")

# ✅ 既存インスタンスチェック（重複作成防止）
instances = compute.list_instances(compartment_id=compartment_id)
for instance in instances.data:
    if instance.display_name == "a1-auto-instance" and \
       instance.lifecycle_state not in ["TERMINATED", "TERMINATING"]:
        print(f"✅ インスタンスはすでに存在します（状態: {instance.lifecycle_state}）。スキップします。")
        exit(0)

print("インスタンスが存在しないため、作成を試みます...")

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
            image_id=image_id,  # ← 追加
            display_name="a1-auto-instance",
            subnet_id=subnet_id,
            create_vnic_details=oci.core.models.CreateVnicDetails(
                assign_public_ip=True,
                subnet_id=subnet_id
            ),
            metadata={
                "ssh_authorized_keys": ssh_public_key
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
