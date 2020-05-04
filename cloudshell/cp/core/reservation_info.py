from dataclasses import dataclass


@dataclass
class ReservationInfo:
    reservation_id: str
    owner: str
    blueprint: str
    domain: str

    @classmethod
    def from_context(cls, context):
        return cls(
            reservation_id=context.reservation_id,
            owner=context.owner_user,
            blueprint=context.environment_name,
            domain=context.domain,
        )
