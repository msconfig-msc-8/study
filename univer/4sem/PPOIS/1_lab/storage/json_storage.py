from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

from models.agency import Agency
from models.agent import Agent
from models.client import Client
from models.deal import Deal
from models.document import Document
from models.market import Market
from models.property import Property


DATA_FILE = Path(__file__).resolve().parent.parent / "data.json"


def has_saved_data(file_path: Path = DATA_FILE) -> bool:
    return file_path.exists()


def backup_data_file(file_path: Path = DATA_FILE) -> Path:
    backup_path = file_path.with_name(
        f"{file_path.stem}_broken_"
        f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        f"{file_path.suffix}"
    )
    file_path.replace(backup_path)
    return backup_path


def save_agency(agency: Agency, file_path: Path = DATA_FILE) -> None:
    data = {
        "agency": {
            "name": agency.name,
        },
        "market": {
            "name": agency.market.name,
            "trend_multiplier": agency.market.trend_multiplier,
        },
        "agents": [
            {
                "agent_id": agent.agent_id,
                "name": agent.name,
                "experience_years": agent.experience_years,
            }
            for agent in agency.agents
        ],
        "clients": [
            {
                "client_id": client.client_id,
                "name": client.name,
                "budget": client.budget,
            }
            for client in agency.clients
        ],
        "properties": [
            {
                "property_id": property_obj.property_id,
                "address": property_obj.address,
                "price": property_obj.price,
                "area": property_obj.area,
                "is_available": property_obj.is_available,
            }
            for property_obj in agency.properties
        ],
        "documents": [
            {
                "document_id": document.document_id,
                "client_id": document.client.client_id,
                "agent_id": document.agent.agent_id,
                "property_id": document.property_obj.property_id,
                "created_at": document.created_at.isoformat(),
                "is_signed": document.is_signed,
            }
            for document in agency.documents
        ],
        "deals": [
            {
                "deal_id": deal.deal_id,
                "client_id": deal.client.client_id,
                "agent_id": deal.agent.agent_id,
                "property_id": deal.property_obj.property_id,
                "document_id": (
                    deal.document.document_id if deal.document is not None else None
                ),
                "final_price": deal.final_price,
                "created_at": deal.created_at.isoformat(),
                "completed_at": (
                    deal.completed_at.isoformat()
                    if deal.completed_at is not None
                    else None
                ),
                "is_completed": deal.is_completed,
            }
            for deal in agency.deals
        ],
    }

    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = file_path.with_suffix(f"{file_path.suffix}.tmp")
    temp_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(file_path)


def load_agency(file_path: Path = DATA_FILE) -> Agency:
    data = json.loads(file_path.read_text(encoding="utf-8"))

    market_data = data["market"]
    market = Market(
        market_data["name"],
        float(market_data["trend_multiplier"]),
    )
    agency = Agency(data["agency"]["name"], market)

    for agent_data in data.get("agents", []):
        agency.add_agent(
            Agent(
                int(agent_data["agent_id"]),
                agent_data["name"],
                int(agent_data["experience_years"]),
            )
        )

    for client_data in data.get("clients", []):
        agency.add_client(
            Client(
                int(client_data["client_id"]),
                client_data["name"],
                float(client_data["budget"]),
            )
        )

    for property_data in data.get("properties", []):
        property_obj = Property(
            int(property_data["property_id"]),
            property_data["address"],
            float(property_data["price"]),
            float(property_data["area"]),
        )
        property_obj.is_available = bool(property_data["is_available"])
        agency.add_property(property_obj)

    documents_by_id = _load_documents(agency, data.get("documents", []))
    _load_deals(agency, data.get("deals", []), documents_by_id)

    return agency


def _load_documents(
    agency: Agency,
    documents_data: list[dict[str, Any]],
) -> dict[int, Document]:
    documents_by_id: dict[int, Document] = {}

    for document_data in documents_data:
        document = Document(
            int(document_data["document_id"]),
            agency.get_client_by_id(int(document_data["client_id"])),
            agency.get_agent_by_id(int(document_data["agent_id"])),
            agency.get_property_by_id(int(document_data["property_id"])),
        )
        document.created_at = datetime.datetime.fromisoformat(
            document_data["created_at"]
        )
        document.is_signed = bool(document_data["is_signed"])

        agency.add_document(document)
        documents_by_id[document.document_id] = document

    return documents_by_id


def _load_deals(
    agency: Agency,
    deals_data: list[dict[str, Any]],
    documents_by_id: dict[int, Document],
) -> None:
    for deal_data in deals_data:
        deal = Deal(
            int(deal_data["deal_id"]),
            agency.get_property_by_id(int(deal_data["property_id"])),
            agency.get_client_by_id(int(deal_data["client_id"])),
            agency.get_agent_by_id(int(deal_data["agent_id"])),
            float(deal_data["final_price"]),
        )
        deal.created_at = datetime.datetime.fromisoformat(
            deal_data["created_at"]
        )

        completed_at = deal_data.get("completed_at")
        if completed_at is not None:
            deal.completed_at = datetime.datetime.fromisoformat(completed_at)

        deal.is_completed = bool(deal_data["is_completed"])

        document_id = deal_data.get("document_id")
        if document_id is not None:
            deal.document = documents_by_id[int(document_id)]

        agency.add_deal(deal)
