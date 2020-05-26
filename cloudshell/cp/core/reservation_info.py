from dataclasses import dataclass


@dataclass
class ReservationInfo:
    reservation_id: str
    owner: str
    blueprint: str
    domain: str

    @classmethod
    def _from_reservation_context(cls, reservation):
        return cls(
            reservation_id=reservation.reservation_id,
            owner=reservation.owner_user,
            blueprint=reservation.environment_name,
            domain=reservation.domain,
        )

    @classmethod
    def from_resource_context(cls, context):
        """

        :param context:
        :return:
        """
        return cls._from_reservation_context(reservation=context.reservation)

    @classmethod
    def from_remote_resource_context(cls, context):
        """

        :param context:
        :return:
        """
        return cls._from_reservation_context(reservation=context.remote_reservation)

