﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject playerCamera;
    public GameObject battleCamera;

    public GameObject player;

    public List<BasePokemon> allPokemon = new List<BasePokemon>();
    public List<BasePokemon> allPlayerPokemon = new List<BasePokemon>();

    public List<PokemonMoves> allMoves = new List<PokemonMoves>();

    public Transform defencePodium;
    public Transform attackPodium;
    public GameObject emptyPokemon;
    public BasePokemon battlePokemon;

    public BattleManager battleManager;

    private GameObject defPokemon;
    public GameObject atkPokemon;

    // Start is called before the first frame update
    void Start()
    {
        playerCamera.SetActive(true);
        battleCamera.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void EnterBattle(Rarity rarity)
    {
        battleManager.humanEnemy = false;

        playerCamera.SetActive(false);
        battleCamera.SetActive(true);

        battlePokemon = GetRandomPokemonFromList(GetPokemonByRarity(rarity));
        battleManager.enemyHealthBar.localScale = new Vector3(1, 1, 1);

        battlePokemon.HP = battlePokemon.maxHP;

        Debug.Log(battlePokemon.pName);

        player.GetComponent<PlayerMovement>().isAllowedToMove = false;

        defPokemon = Instantiate(emptyPokemon, defencePodium.transform.position, Quaternion.identity);

        Vector3 pokeLocalPos = new Vector3(0, 1, 0);

        defPokemon.transform.parent = defencePodium;
        defPokemon.transform.localPosition = pokeLocalPos;

        BasePokemon tempPokemon = defPokemon.AddComponent<BasePokemon>() as BasePokemon;
        tempPokemon.AddMember(battlePokemon);

        defPokemon.GetComponent<SpriteRenderer>().sprite = battlePokemon.image;

        battleManager.ChangeMenu(BattleMenu.Selection);
    }

    public void DisplayPlayerPokemon(BasePokemon playerPokemon)
    {
        atkPokemon = Instantiate(emptyPokemon, attackPodium.transform.position, Quaternion.identity);

        Vector3 pokeLocalPos = new Vector3(0, 1, 0);

        atkPokemon.transform.parent = attackPodium;
        atkPokemon.transform.localPosition = pokeLocalPos;

        BasePokemon tempPokemon = atkPokemon.AddComponent<BasePokemon>() as BasePokemon;
        tempPokemon.AddMember(playerPokemon);

        atkPokemon.GetComponent<SpriteRenderer>().sprite = playerPokemon.image;
    }

    public void ExitBattle()
    {
        battleCamera.SetActive(false);
        playerCamera.SetActive(true);
        player.GetComponent<PlayerMovement>().isAllowedToMove = true;
        defPokemon.GetComponent<SpriteRenderer>().sprite = null;
    }

    public List<BasePokemon> GetPokemonByRarity(Rarity rarity)
    {
        List<BasePokemon> returnPokemon = new List<BasePokemon>();

        foreach(BasePokemon pokemon in allPokemon)
        {
            if(pokemon.rarity == rarity)
            {
                returnPokemon.Add(pokemon);
            }
        }

        return returnPokemon;
    }

    public BasePokemon GetRandomPokemonFromList(List<BasePokemon> pokeList)
    {
        BasePokemon pokemon = new BasePokemon();
        int pokemonIndex = Random.Range(0, pokeList.Count - 1);
        pokemon = pokeList[pokemonIndex];
        return pokemon;
    }
}

[System.Serializable]
public class PokemonMoves
{
    public string Name;
    public MoveType category;
    public Stat moveStat;
    public PokemonType moveType;
    public int pp;
    public int currentPP;
    public float power;
    public float accuracy;
}

[System.Serializable] 
public class Stat
{
    public float minimum;
    public float maximum;
}

public enum MoveType
{
    Physical,
    Special,
    Status
}
