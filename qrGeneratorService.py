import qrcode
from PIL import Image
import os
import properties
import access


class qrGeneratorService:
    def generate_qr(self,voter_id):
        print(self.voter_id)
        os.makedirs("qr_codes", exist_ok=True)
        file_path = f"qr_codes/{self.voter_id}.png"

        qr = qrcode.make(self.voter_id)
        qr.save(file_path)
        print(self.voter_id)
        connection,cursor = access.dbUtils.get_connection(self)
        cursor.execute(properties.update_qr_status, {"voter_id": self.voter_id})
        connection.commit()

        
        return file_path
        

        access.dbUtils.close_connection(self)