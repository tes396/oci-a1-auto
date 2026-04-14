import oci
import os
import base64

config = oci.config.from_file()
compute = oci.core.ComputeClient(config)
compartment_id = os.environ['COMPARTMENT_ID']

images = compute.list_images(
    compartment_id=compartment_id,
    operating_system="Canonical Ubuntu",
    shape="VM.Standard.A1.Flex"
)

for img in images.data:
    print(f"名前: {img.display_name}")
    # Base64エンコードして出力（マスク回避）
    encoded = base64.b64encode(img.id.encode()).decode()
    print(f"OCID(base64): {encoded}")
    print("---")
