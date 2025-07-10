from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random
from shared_state import estado_agentes as shared_estado_agentes

class AvionAgent(Agent):
    class VueloBehaviour(CyclicBehaviour):
        async def on_start(self):
            self.aterrizado = False
            if shared_estado_agentes is not None:
                shared_estado_agentes[self.agent.name] = "Volando"
            print(f"[{self.agent.name}] Comenzando comportamiento de vuelo.")

        async def run(self):
            if self.aterrizado:
                return

            if shared_estado_agentes is not None:
                shared_estado_agentes[self.agent.name] = "Volando"
            print(f"[{self.agent.name}] Está volando...")
            await asyncio.sleep(random.randint(2, 4))

            msg = Message(to=self.agent.torre_jid)
            msg.body = "SOLICITUD_ATERRIZAJE"
            await self.send(msg)
            print(f"[{self.agent.name}] Solicita aterrizar.")
            if shared_estado_agentes is not None:
                shared_estado_agentes[self.agent.name] = "Solicita aterrizaje"

            msg = await self.receive(timeout=5)
            if msg:
                if msg.body == "PERMISO_OTORGADO":
                    print(f"[{self.agent.name}] Aterrizando...")
                    if shared_estado_agentes is not None:
                        shared_estado_agentes[self.agent.name] = "Aterrizando"
                    self.aterrizado = True
                elif msg.body == "PISTA_OCUPADA":
                    print(f"[{self.agent.name}] Esperando para intentar de nuevo...")
                    if shared_estado_agentes is not None:
                        shared_estado_agentes[self.agent.name] = "Esperando"
                    await asyncio.sleep(3)

    async def setup(self):
        print(f"[{self.name}] Agente avión iniciado.")
        self.torre_jid = "torre@localhost"
        self.add_behaviour(self.VueloBehaviour())
