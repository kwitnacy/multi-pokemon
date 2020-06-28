using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public List<BasePokemon> ownedPokemon = new List<BasePokemon>();
    public BasePokemon defaultPokemon;

    // Start is called before the first frame update
    void Start()
    {
        foreach(BasePokemon pokemon in ownedPokemon)
        {
            pokemon.HP = pokemon.maxHP;
        }
        defaultPokemon.HP = defaultPokemon.maxHP;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void CatchPokemon(BasePokemon defeatedPokemon)
    {
        if (defeatedPokemon.pName != defaultPokemon.pName)
        {
            foreach (BasePokemon pokemon in ownedPokemon)
            {
                if (pokemon.pName == defeatedPokemon.pName)
                {
                    pokemon.canBeUsedByPlayer = true;
                    break;
                }
            }
        }
    }

    public void CatchPokemon(string defeatedPokemonName)
    {
        if (defeatedPokemonName != defaultPokemon.pName)
        {
            foreach (BasePokemon pokemon in ownedPokemon)
            {
                if (pokemon.pName == defeatedPokemonName)
                {
                    pokemon.canBeUsedByPlayer = true;
                    break;
                }
            }
        }
    }

    /// Returns true if was successful
    public bool ChangeDefaultPokemon(int pokemonIndex)
    {
        if(ownedPokemon[pokemonIndex].canBeUsedByPlayer)
        {
            ownedPokemon.Add(defaultPokemon);
            defaultPokemon = ownedPokemon[pokemonIndex];
            ownedPokemon.Remove(ownedPokemon[pokemonIndex]);
            return true;
        }
        else
        {
            return false;
        }
    }

    /// If there is none returns -1
    public int PickFirstAvailablePokemon()
    {
        for(int i = 0; i < ownedPokemon.Count; i++)
        {
            if(ownedPokemon[i].canBeUsedByPlayer)
            {
                return i;
            }
        }
        return -1;
    }
}

[System.Serializable]
public class OwnedPokemon
{
    public string nickName;
    public BasePokemon pokemon;
    public int level;
    // public List<PokemonMoves> moves = new List<PokemonMoves>();
}
