import discord

from utils import models
from typing import Optional


# Easy API
async def register_guild(guild: discord.Guild):
    await add_guild_if_not_exist(guild.id)


async def is_member_registered(member: discord.Member) -> bool:
    member = await get_member(member.id)
    if not member:
        return False

    return True


async def register_member(member: discord.Member):
    await add_member_if_not_exist(member.id)
    await add_guildmember_if_not_exist(member.guild.id, member.id)


async def register_guildmember(member: discord.Member):
    await add_guild_if_not_exist(member.guild.id, member.id)

# Hidden
async def get_guild(guild_id: int) -> Optional[models.Guild]:
    return await models.Guild.query.where(models.Guild.id == guild_id).gino.first()


async def add_guild(guild_id: int) -> models.Guild:
    return await models.Guild.create(id=guild_id)


async def add_guild_if_not_exist(guild_id: int) -> models.Guild:
    guild = await get_guild(guild_id)
    if not guild:
       guild = await add_guild(guild_id)
    return guild


async def get_member(member_id: int) -> Optional[models.Member]:
    return await models.Member.query.where(models.Member.id == member_id).gino.first()


async def add_member(member_id: int) -> models.Member:
    return await models.Member.create(id=member_id)


async def add_member_if_not_exist(member_id: int) -> models.Member:
    member = await get_member(member_id)
    if not member:
        member = await add_member(member_id)
    return member


async def get_guildmember(guild_id: int, member_id: int) -> Optional[models.GuildMember]:
    return await models.GuildMember.query.where((models.GuildMember.guild_id == guild_id) & (models.GuildMember.member_id == member_id)).gino.first()


async def add_guildmember(guild_id: int, member_id: int) -> models.GuildMember:
    return await models.GuildMember.create(guild_id=guild_id, member_id=member_id)


async def add_guildmember_if_not_exist(guild_id: int, member_id: int) -> models.GuildMember:
    guildmember = await get_guildmember(guild_id, member_id)
    if not guildmember:
        guildmember = await add_guildmember(guild_id, member_id)
    return guildmember
