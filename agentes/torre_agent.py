from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio

class TorreControlAgent(Agent):
    class ControlBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.pista_libre = True

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[TORRE] Mensaje recibido de {msg.sender}: {msg.body}")

                if msg.body == "SOLICITUD_ATERRIZAJE":
                    reply = Message(to=str(msg.sender))
                    if self.pista_libre:
                        reply.body = "PERMISO_OTORGADO"
                        self.pista_libre = False
                        print("[TORRE] Permiso concedido.")
                        await self.send(reply)

                        await asyncio.sleep(5)
                        self.pista_libre = True
                        print("[TORRE] Pista libre nuevamente.")
                    else:
                        reply.body = "PISTA_OCUPADA"
                        print("[TORRE] Pista ocupada.")
                        await self.send(reply)

    async def setup(self):
        print("[TORRE] Agente torre iniciado.")
        self.add_behaviour(self.ControlBehaviour())
