import pytest
import asyncio


@pytest.mark.anyio
async def test_deposit(client, wallet):

    responce = await client.post(
        f"/api/v1/wallets/{wallet}/operation",
        json={"operation_type": "DEPOSIT", "amount": 100},
    )

    assert responce.status_code == 200
    data = responce.json()
    assert data["balance"] == 100


@pytest.mark.anyio
async def test_withdraw(client, wallet):

    await client.post(
        f"/api/v1/wallets/{wallet}/operation",
        json={"operation_type": "DEPOSIT", "amount": 200},
    )

    responce = await client.post(
        f"/api/v1/wallets/{wallet}/operation",
        json={"operation_type": "WITHDRAW", "amount": 100},
    )

    data = responce.json()

    assert data["balance"] == 100


@pytest.mark.anyio
async def test_negative_balance(client, wallet):
    responce = await client.post(
        f"/api/v1/wallets/{wallet}/operation",
        json={"operation_type": "WITHDRAW", "amount": 100},
    )

    assert responce.status_code in (400, 422)


@pytest.mark.anyio
async def test_concurence_deposits(client, wallet):
    async def deposit():
        return await client.post(
            f"/api/v1/wallets/{wallet}/operation",
            json={"operation_type": "DEPOSIT", "amount": 10},
        )

    tasks = [deposit() for _ in range(10)]

    responces = await asyncio.gather(*tasks)

    for responce in responces:
        assert responce.status_code == 200

    balance = await client.get(f"/api/v1/wallets/{wallet}")

    assert balance.json()["balance"] == 100
