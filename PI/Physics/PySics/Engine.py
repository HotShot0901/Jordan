from .Utility   import *
from .RigidBody import *
from .Colliders import *

class PySics:
    __Bodies: List[RigidBody]

    __BulletWorld : Any
    __BulletNodes : List

    Gravity: pyrr.Vector3

    def __init__(self) -> None:
        self.__BulletWorld = BulletWorld()
        self.__Bodies = []
        self.Gravity = pyrr.Vector3([ 0, -9.81, 0 ])

        g = self.Gravity
        self.__BulletWorld.setGravity(Vec3(g.x, g.y, g.z))
        
        self.__BulletNodes = []

    def AddRigidBody(self, body: RigidBody) -> Any:
        self.__Bodies.append(body)

        node = BulletRigidBodyNode("RB")

        pos, rot, scale = body.Position, body.Rotation, body.Collider.Scale

        node.setTransform(TransformState.make_pos_hpr_scale(
            Point3(pos.x, pos.y, pos.z),
            Vec3(rot.x, rot.y, rot.z),
            Vec3(scale.x, scale.y, scale.z)
        ))

        bounds = body.Collider.Bounds
        if isinstance(body.Collider, BoxCollider):
            shape = BulletBoxShape(Vec3(bounds.x, bounds.y, bounds.z))
        elif isinstance(body.Collider, PlaneCollider):
            shape = BulletPlaneShape(
                Vec3(body.Collider.Up.x, body.Collider.Up.y, body.Collider.Up.z),
                bounds.x
            )

        node.addShape(shape)
        node.setMass(body.Mass)

        if body.CCD:
            node.setCcdMotionThreshold(1e-7)
            node.setCcdSweptSphereRadius(0.50)

        self.__BulletWorld.attachRigidBody(node)
        self.__BulletNodes.append(node)
        body._Node = node
        return node

    def CreateRigidBody(self, mat: PySicsMaterial) -> RigidBody:
        body = RigidBody(mat)
        self.AddRigidBody(body)
        return body

    def DeleteRigidBody(self, rb: RigidBody) -> None:
        self.__Bodies.remove(rb)
        self.__BulletNodes.remove(rb._Node)
        self.__BulletWorld.removeRigidBody(rb._Node)

    def OnSimulationStart(self) -> None: ...

    def Update(self, dt: float) -> None:
        # Set variables

        # Update bullet physics
        self.__BulletWorld.doPhysics(dt, 10, 1/180)

        # Get variables
        for pySicsBody, bulletBody in zip(self.__Bodies, self.__BulletNodes):
            centralForce = pySicsBody.CentralForce
            bulletBody.applyCentralForce(Vec3(
                centralForce.x, centralForce.y, centralForce.z
            ))
            pySicsBody._SetCentralForce()

            vel = bulletBody.getLinearVelocity()
            pos = bulletBody.getTransform().getPos()
            rot = bulletBody.getTransform().getHpr()

            # Velocity
            pySicsBody.Velocity.x = vel.x
            pySicsBody.Velocity.y = vel.y
            pySicsBody.Velocity.z = vel.z

            # Position
            pySicsBody.Position.x = pos.x
            pySicsBody.Position.y = pos.y
            pySicsBody.Position.z = pos.z

            # Rotation
            pySicsBody.Rotation.x = rot.x
            pySicsBody.Rotation.y = rot.y
            pySicsBody.Rotation.z = rot.z

    def OnSimulationEnd(self) -> None: ...
