import discord

from utils import models
from typing import Optional


async def get_member(member_id: int) -> Optional[models.Member]:
    return await models.Member.query.where(models.Member.id == member_id).gino.first()


async def add_member(member_id: int) -> models.Member:
    return await models.Member.create(id=member_id)


async def add_member_if_not_exist(member_id: int) -> models.Member:
    member = await get_member(member_id)
    if not member:
        member = await add_member(member_id)
    return member


async def add_memberjoinlog(member_id: int) -> models.MemberJoinLog:
    await add_member_if_not_exist(member_id)
    return await models.MemberJoinLog.create(member_id=member_id)


async def add_memberleavelog(member_id: int) -> models.MemberLeaveLog:
    await add_member_if_not_exist(member_id)
    return await models.MemberLeaveLog.create(member_id=member_id)
