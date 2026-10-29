"""
AI Image Analysis Service for WearableLens AI

Handles image analysis through external AI providers with fallback to manual search.
Never fabricates product information or claims certainty without verification.
"""

import base64
import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class AnalysisResult:
    """Structured result from AI image analysis."""

    def __init__(
        self,
        success: bool = False,
        product_name: str = "Unknown",
        manufacturer: str = "Unknown",
        category: str = "Wearable Device",
        confidence: float = 0.0,
        possible_matches: List[Dict[str, Any]] = None,
        facts: Dict[str, Any] = None,
        requires_verification: bool = True,
        error_message: str = None,
    ):
        self.success = success
        self.product_name = product_name
        self.manufacturer = manufacturer
        self.category = category
        self.confidence = confidence
        self.possible_matches = possible_matches or []
        self.facts = facts or {}
        self.requires_verification = requires_verification
        self.error_message = error_message

    def is_verified(self) -> bool:
        """Check if results have verified facts."""
        return not self.requires_verification and self.confidence >= 0.8

    def get_confidence_label(self) -> str:
        """Get human-readable confidence label."""
        if self.confidence >= 0.9:
            return "Very High"
        elif self.confidence >= 0.75:
            return "High"
        elif self.confidence >= 0.5:
            return "Moderate"
        elif self.confidence > 0:
            return "Low"
        return "None"


class AIProvider:
    """Base class for AI image analysis providers."""

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.provider_name = config.get("provider", "unknown")

    def analyze_image(self, image_data: bytes, filename: str) -> AnalysisResult:
        """Analyze an image and return results. Must be implemented by subclasses."""
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    """OpenAI GPT-4V provider for image analysis."""

    def __init__(self, config: Dict[str, str]):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "gpt-4-vision-preview")
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def analyze_image(self, image_data: bytes, filename: str) -> AnalysisResult:
        """Analyze image using OpenAI GPT-4V."""
        if not self.api_key:
            return AnalysisResult(
                success=False,
                error_message="OpenAI API key not configured",
            )

        try:
            # Convert image to base64
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Prepare the message for GPT-4V
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this image for a wearable electronic device. Look at:
- The device shape and form factor
- Where it appears to be worn (head, wrist, body, etc.)
- Visible branding, logos, or labels
- Color and materials
- Any distinctive features or placement details

Provide a structured analysis with:
1. Most likely product name(s) and confidence (0-1)
2. Manufacturer if identifiable
3. Product category
4. Intended use/purpose
5. Key features visible
6. Estimated price range if discernible

Be honest - if you cannot identify the device, state that clearly. 
Confidence levels 0.9-1.0 = very confident identification
Confidence levels 0.7-0.89 = likely match
Confidence levels 0.5-0.69 = possible match, needs verification
Confidence levels below 0.5 = insufficient data for reliable identification

Return JSON format with keys: product_name, manufacturer, category, confidence, possible_matches[], notes
""",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high",
                            },
                        },
                    ],
                }
            ]

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 1000,
            }

            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result_data = response.json()["choices"][0]["message"]["content"]

            # Try to parse JSON from the response
            analysis = self._parse_ai_response(result_data)

            if analysis and analysis.get("success"):
                return AnalysisResult(
                    success=True,
                    product_name=analysis.get("product_name", "Unknown"),
                    manufacturer=analysis.get("manufacturer", "Unknown"),
                    category=analysis.get("category", "Wearable Device"),
                    confidence=analysis.get("confidence", 0.0),
                    possible_matches=analysis.get("possible_matches", []),
                    facts=analysis.get("facts", {}),
                    requires_verification=analysis.get("requires_verification", True),
                )
            else:
                return AnalysisResult(
                    success=False,
                    error_message=analysis.get("error", "Failed to parse AI response"),
                    requires_verification=True,
                )

        except requests.exceptions.Timeout:
            logger.error("OpenAI API request timed out")
            return AnalysisResult(
                success=False,
                error_message="Analysis request timed out. Please try again.",
                requires_verification=True,
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAI API request error: {e}")
            return AnalysisResult(
                success=False,
                error_message=f"AI service error: {str(e)[:100]}",
                requires_verification=True,
            )
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return AnalysisResult(
                success=False,
                error_message="Failed to parse analysis response",
                requires_verification=True,
            )
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI analysis: {e}")
            return AnalysisResult(
                success=False,
                error_message="Unexpected analysis error",
                requires_verification=True,
            )

    def _parse_ai_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse JSON from AI response, handling various formats."""
        try:
            # Try direct JSON parse
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code blocks
        import re

        markdown_pattern = r"```json\s*(\{.*?\})\s*```"
        match = re.search(markdown_pattern, response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # Try to find JSON object in text
        brace_start = response_text.find("{")
        if brace_start >= 0:
            try:
                # Find matching closing brace
                depth = 0
                for i in range(brace_start, len(response_text)):
                    if response_text[i] == "{":
                        depth += 1
                    elif response_text[i] == "}":
                        depth -= 1
                        if depth == 0:
                            json_str = response_text[brace_start : i + 1]
                            return json.loads(json_str)
                            break
            except Exception:
                pass

        return None


class GoogleGeminiProvider(AIProvider):
    """Google Gemini Vision provider for image analysis."""

    def __init__(self, config: Dict[str, str]):
        super().__init__(config)
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "gemini-pro-vision")
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models:{self.model}:generateContent"

    def analyze_image(self, image_data: bytes, filename: str) -> AnalysisResult:
        """Analyze image using Google Gemini Vision."""
        if not self.api_key:
            return AnalysisResult(
                success=False,
                error_message="Google AI API key not configured",
            )

        try:
            base64_image = base64.b64encode(image_data).decode("utf-8")

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": """Analyze this image for a wearable electronic device. Provide analysis in JSON with:
- product_name: most likely product or "Unknown"
- manufacturer: if identifiable or "Unknown" 
- category: product category
- confidence: 0-1 confidence score
- possible_matches: array of possible devices with their confidence levels
- notes: any observations about the device features

If the device cannot be identified from the image, set confidence to 0 and list "insufficient_data" as the only note.

Be transparent about identification limits.
""",
                                "image": {
                                    "mime_type": "image/jpeg",
                                    "data": base64_image,
                                },
                            },
                        ],
                    }
                ],
                "temperature": 0.1,
            }

            url = f"{self.endpoint}?key={self.api_key}"
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Parse Gemini response
            if result.get("candidates") and len(result["candidates"]) > 0:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return self._parse_gemini_response(content)
            else:
                return AnalysisResult(
                    success=False,
                    error_message="No analysis result from Gemini API",
                    requires_verification=True,
                )

        except requests.exceptions.Timeout:
            return AnalysisResult(
                success=False,
                error_message="Analysis request timed out",
                requires_verification=True,
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API error: {e}")
            return AnalysisResult(
                success=False,
                error_message=f"AI service error: {str(e)[:100]}",
                requires_verification=True,
            )
        except Exception as e:
            logger.error(f"Unexpected Gemini error: {e}")
            return AnalysisResult(
                success=False,
                error_message="Unexpected analysis error",
                requires_veribration=True,
            )

    def _parse_gemini_response(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse Gemini response text into structured data."""
        import re

        # Try to find JSON in the response
        # Look for JSON object
        brace_pos = text.find("{")
        if brace_pos >= 0:
            try:
                # Find the complete JSON object
                depth = 0
                end_pos = brace_pos
                for i in range(brace_pos, len(text)):
                    if text[i] == "{":
                        depth += 1
                    elif text[i] == "}":
                        depth -= 1
                        if depth == 0:
                            end_pos = i + 1
                            break
                
                json_str = text[brace_pos:end_pos]
                parsed = json.loads(json_str)
                
                # Validate required fields
                if "product_name" in parsed or "confidence" in parsed:
                    return parsed
            except (json.JSONDecodeError, IndexError):
                pass

        # Try regex to find confidence and product name
        confidence_match = re.search(r'confidence[\\s:]*:[\\s]*([0-9]*\\.?[0-9]+)', text, re.I)
        product_match = re.search(r'product.name?[\\s:]*:[\\s]*["\']?([^"\',.]+)["\']?', text, re.I)
        
        confidence = float(confidence_match.group(1)) if confidence_match else 0.0
        product_name = product_match.group(1).strip() if product_match else "Unknown"
        
        return {
            "product_name": product_name,
            "confidence": confidence,
            "requires_verification": confidence < 0.8,
        }


class CustomProvider(AIProvider):
    """Custom API provider for arbitrary image analysis services."""

    def __init__(self, config: Dict[str, str]):
        super().__init__(config)
        self.api_url = config.get("api_url", "")
        self.api_key = config.get("api_key", "")

    def analyze_image(self, image_data: bytes, filename: str) -> AnalysisResult:
        """Analyze image using custom API."""
        if not self.api_url:
            return AnalysisResult(
                success=False,
                error_message="Custom API URL not configured",
            )

        try:
            base64_image = base64.b64encode(image_data).decode("utf-8")

            headers = {
                "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                "Content-Type": "application/json",
            }

            payload = {
                "image": base64_image,
                "filename": filename,
                "analysis_type": "wearable_device",
            }

            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result_data = response.json()
            return self._parse_custom_response(result_data)

        except Exception as e:
            logger.error(f"Custom provider error: {e}")
            return AnalysisResult(
                success=False,
                error_message=f"Custom API error: {str(e)[:100]}",
                requires_verification=True,
            )

    def _parse_custom_response(self, data: Any) -> AnalysisResult:
        """Parse custom API response. Override as needed."""
        return AnalysisResult(
            success=True,
            product_name=data.get("product_name", "Unknown"),
            confidence=float(data.get("confidence", 0.0)),
            requires_verification=data.get("requires_verification", True),
        )


# Provider factory
def create_provider(config: Dict[str, str]) -> Optional[AIProvider]:
    """Create an AI provider instance based on configuration."""
    provider_type = config.get("provider", "none").lower()

    if provider_type == "openai":
        return OpenAIProvider(config)
    elif provider_type == "google":
        return GoogleGeminiProvider(config)
    elif provider_type == "custom":
        return CustomProvider(config)
    elif provider_type in ("none", ""):
        return None
    else:
        logger.warning(f"Unknown AI provider: {provider_type}")
        return None


# Manual search fallback
def generate_manual_search_guidance(image_features: Dict[str, str]) -> Dict[str, Any]:
    """Generate manual search guidance when AI analysis is unavailable.
    
    This provides structured search suggestions based on observable features
    without fabricating product information.
    """
    features = image_features or {}
    
    guidance = {
        "search_terms": [],
        "categories": [],
        "visual_hints": [],
        "manual_checklist": [],
    }
    
    # Analyze visible features
    placement = features.get("placement", "").lower()
    shape = features.get("shape", "").lower()
    color = features.get("color", "").lower()
    branding = features.get("branding", "").lower()
    materials = features.get("materials", "").lower()
    
    # Generate search terms based on placement
    if "temple" in placement or "side" in placement or "head" in placement:
        guidance["search_terms"].extend([
            "temple-mounted wearable device",
            "side-of-head electronic device",
            "ear temple technology",
        ])
        guidance["categories"].append("Head-worn wearable")
    
    if "glass" in shape or "lens" in shape:
        guidance["search_terms"].extend([
            "smart glasses accessory",
            "wearable camera",
        ])
        guidance["categories"].append("Smart glasses/optical")
    
    if "camera" in features.get("description", "").lower():
        guidance["search_terms"].append("miniature camera wearable")
    
    # Add visual hints
    if color:
        guidance["visual_hints"].append(f"{color} colored device")
    if branding:
        guidance["visual_hints"].append(f"Branding: {branding}")
    if "metal" in materials:
        guidance["visual_hints"].append("Metal construction")
    if "plastic" in materials or "polycarbonate" in materials:
        guidance["visual_hints"].append("Plastic/composite construction")
    
    # Manual verification checklist
    guidance["manual_checklist"] = [
        "Search online marketplaces for described features",
        "Check for regulatory certifications (FCC, CE, etc.)",
        "Look for manufacturer logos or model numbers",
        "Verify compatibility with your use case",
        "Check recent reviews and user reports",
    ]
    
    return guidance