"""Module providing abstract Node2Vec implementation."""

from typing import Dict, Any
from ensmallen import Graph
import pandas as pd
from userinput.utils import must_be_in_set
from ensmallen import models
from embiggen.utils.abstract_models import abstract_class
from embiggen.embedders.ensmallen_embedders.ensmallen_embedder import EnsmallenEmbedder
from embiggen.utils import EmbeddingResult, normalize_kwargs


@abstract_class
class Node2VecEnsmallen(EnsmallenEmbedder):
    """Abstract class for Node2Vec algorithms."""

    MODELS = {
        "DeepWalk CBOW": models.CBOW,
        "DeepWalk SkipGram": models.SkipGram,
        "DeepWalk GloVe": models.GloVe,
        "Node2Vec CBOW": models.CBOW,
        "Node2Vec SkipGram": models.SkipGram,
        "Node2Vec GloVe": models.GloVe,
        "Node2Vec Dreamwalk": models.DreamWalk,  # refers to ensmallen.bindings Node2VecBinding.DreamWalk (which is a Rust-struct with python bindings)
        "Walklets CBOW": models.WalkletsCBOW,
        "Walklets SkipGram": models.WalkletsSkipGram,
        "Walklets GloVe": models.WalkletsGloVe,
    }

    def __init__(
        self,
        embedding_size: int = 100,
        random_state: int = 42,
        ring_bell: bool = False,
        enable_cache: bool = False,
        **model_kwargs: Dict,
    ):
        """Create new abstract Node2Vec method.

        Parameters
        --------------------------
        embedding_size: int = 100
            Dimension of the embedding.
        random_state: int = 42
            The random state to reproduce the training sequence.
        ring_bell: bool = False,
            Whether to play a sound when embedding completes.
        enable_cache: bool = False
            Whether to enable the cache, that is to
            store the computed embedding.
        model_kwargs: Dict
            Further parameters to forward to the model.
        """
        model_name = must_be_in_set(self.model_name(), self.MODELS.keys(), "model name")
        self._model_kwargs = normalize_kwargs(
            self,
            {
                **model_kwargs,
                "embedding_size": embedding_size,
                "random_state": random_state,
            },
        )

        embedding_size = self._model_kwargs.pop("embedding_size")
        random_state = self._model_kwargs.pop("random_state")

        self._model = Node2VecEnsmallen.MODELS[model_name](
            embedding_size=embedding_size,
            random_state=random_state,
            **self._model_kwargs,
        )

        super().__init__(
            embedding_size=embedding_size,
            enable_cache=enable_cache,
            ring_bell=ring_bell,
            random_state=random_state,
        )

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            epochs=1,
            embedding_size=5,
            window_size=1,
            walk_length=4,
            max_neighbours=10,
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters of the model."""
        return dict(**super().parameters(), **self._model_kwargs)

    def _fit_transform(
        self,
        graph: Graph,
        return_dataframe: bool = True,
    ) -> EmbeddingResult:
        """Return node embedding."""
        # print("hi from Node2VecEnsmallen._fit_transform", self._model)
        node_embeddings = self._model.fit_transform(graph)

        if "CBOW" in self.model_name():
            node_embeddings = list(reversed(node_embeddings))

        if return_dataframe:
            node_names = graph.get_node_names()
            node_embeddings = [
                pd.DataFrame(node_embedding, index=node_names)
                for node_embedding in node_embeddings
            ]
        return EmbeddingResult(
            embedding_method_name=self.model_name(), node_embeddings=node_embeddings
        )

    @classmethod
    def requires_edge_weights(cls) -> bool:
        return False

    @classmethod
    def requires_positive_edge_weights(cls) -> bool:
        return True

    @classmethod
    def can_use_edge_weights(cls) -> bool:
        """Returns whether the model can optionally use edge weights."""
        return True

    def is_using_edge_weights(self) -> bool:
        """Returns whether the model is parametrized to use edge weights."""
        return True

    @classmethod
    def can_use_node_types(cls) -> bool:
        """Returns whether the model can optionally use node types."""
        return True

    def is_using_node_types(self) -> bool:
        """Returns whether the model is parametrized to use node types."""
        return (
            "change_node_type_weight" in self._model_kwargs
            and self._model_kwargs["change_node_type_weight"] != 1.0
        )

    @classmethod
    def can_use_edge_types(cls) -> bool:
        """Returns whether the model can optionally use edge types."""
        return True

    def is_using_edge_types(self) -> bool:
        """Returns whether the model is parametrized to use edge types."""
        return (
            "change_edge_type_weight" in self._model_kwargs
            and self._model_kwargs["change_edge_type_weight"] != 1.0
        )

    @classmethod
    def is_stocastic(cls) -> bool:
        """Returns whether the model is stocastic and has therefore a random state."""
        return True

    @classmethod
    def requires_node_types(cls) -> bool:
        return False

    @classmethod
    def requires_edge_types(cls) -> bool:
        return False
