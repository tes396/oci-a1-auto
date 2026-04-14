import oci
import os

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
    # OCIDを分割して表示（マスク回避）
    ocid = img.id
    print(f"OCID前半: {ocid[:50]}")
    print(f"OCID後半: {ocid[50:]}")
    print("---")
