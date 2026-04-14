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
            availability_domain="YOUR_AD_NAME",  # ← 要変更
            shape="VM.Standard.A1.Flex",
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=4,
                memory_in_gbs=24
            ),
            display_name="a1-auto-instance",
            # 必要に応じてサブネットIDなど追加
        )
    )
    print("✅ インスタンス作成成功！")
    print(response.data)
except oci.exceptions.ServiceError as e:
    if "Out of capacity" in str(e):
        print("⚠️ 容量不足 - 次回再試行します")
    else:
        print(f"エラー: {e}")
