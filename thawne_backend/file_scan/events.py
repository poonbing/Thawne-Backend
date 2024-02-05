from flask_socketio import Namespace, emit
from .utils import file_scan


file_content = (f"TOP SECRET Document Classification: TOP SECRET // EYES ONLY Date: February 5, 2024 Subject: Analysis of Potential Threats from Advanced Cyber Warfare Tactics This document contains highly sensitive and classified information. Unauthorized access, dissemination, or reproduction of any part of this document is strictly prohibited and may result in severe penalties under applicable laws and regulations. This document serves to outline the evolving landscape of advanced cyber warfare tactics and potential threats to national security infrastructure. It is intended for authorized personnel with the appropriate security clearance and need-to-know basis. Recent cyber intelligence indicates a significant increase in sophisticated cyber attacks targeting critical infrastructure and government systems. These attacks exploit vulnerabilities in network security protocols and leverage advanced malware and intrusion techniques. The scope of this document encompasses an analysis of recent cyber attacks, including their tactics, techniques, and procedures. It also highlights potential vulnerabilities within our own systems that adversaries may exploit. Key findings reveal a growing trend of state-sponsored cyber attacks aimed at disrupting essential services, stealing sensitive information, and undermining public trust in government institutions. These attacks pose a significant threat to national security and require immediate attention and mitigation strategies. Implications of these findings include the potential for widespread disruption of critical services such as energy, transportation, and communication networks. Moreover, the compromise of sensitive government data could have far-reaching consequences for national security and diplomatic relations. Recommendations for addressing these threats include enhancing cybersecurity measures, conducting regular threat assessments, and investing in advanced detection and response capabilities. Collaboration with international partners and intelligence sharing are also essential for effectively countering cyber threats on a global scale. To maintain the integrity and confidentiality of this document, the following security measures must be adhered to: Access to this document is restricted to individuals with the appropriate security clearance and need-to-know basis. All copies of this document must be stored in designated secure facilities or containers when not in use. Destruction of this document must be carried out in accordance with established protocols for classified materials. This document must not be discussed or disclosed in unsecured environments. Care must be taken to prevent unauthorized individuals from viewing or accessing the contents of this document. Any suspected or actual compromise of the security of this document must be reported immediately to the appropriate authorities. Distribution of this document is strictly limited to individuals authorized by the issuing authority. Any requests for additional copies or dissemination must be approved through official channels. The information contained in this document is of the utmost sensitivity and importance. It is imperative that all individuals granted access to this document understand and adhere to the strict security protocols outlined herein. [Signature/Stamp of the Issuing Authority] [Classification Markings: TOP SECRET // EYES ONLY]")
file_content1 = "1"
filename = "CFReDS - Data Leakage Case.pdf"


class FileQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.items:
            return self.items.pop(0)
        else:
            return False
    
    def is_empty(self):
        if not self.items:
            return True
        return False

    def size(self):
        return len(self.items)
    
    def peek(self):
        if self.items:
            return self.items[0]
        else:
            return False
        
    def display(self):
        return self.items

class FileScanNamespace(Namespace):
    def on_queue_file(self, data):
        filequeue = FileQueue()
        state = filequeue.is_empty()
        filequeue.enqueue(data)
        if state:
            file_scan(data['user_id'], data['password'],data["filename"], data["file_security"])